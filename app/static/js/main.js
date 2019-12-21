function goToTop() {
	$("html, body").animate({ scrollTop: 0 }, "slow");
}

function getLoadingHTML(id) {
	return `
		<div id="${id}">
			<div class="spinner-border text-warning" role="status"></div>
			<span>Loading...</span>
		</div>`;
}

function search() {
	let key = $("#select-query-basis")
		.find("option:selected")
		.html();
	let value = "";
	if (key === "时间")
		value = $("#search-input")
			.val()
			.split("/")
			.join("");
	else if (key === "原因" || key === "结果") value = $("#search-input").val();
	else
		value = $("#select-attr-value")
			.find("option:selected")
			.html();
	if (key && value) {
		$(".pager>ul").html("");
		$("main>div").html(getLoadingHTML("loading-events-card"));
		$.get(`/events_intro?key=${key}&value=${value}&page=1`, data => {
			showSearchedEventCards(1, data, key, value);
		});
	}
}

function modifySearchInputElement(obj) {
	// 根据 查询依据 修改 #search-input
	setTimeout(() => {
		queryBasis = obj.currentTarget.querySelector("a > span:last-child")
			.innerHTML;

		$("aside > div")
			.children()[0]
			.remove();
		if (queryBasis === "时间") {
			$("aside > div").prepend(
				'<input type="search" id="search-input" class="form-control" placeholder="示例：2017/08/26" />'
			);
			$("#search-input").keypress(event => {
				if (event.keyCode === 13) search();
			});
		} else if (queryBasis === "原因" || queryBasis === "结果") {
			$("aside > div").prepend(
				'<input type="search" id="search-input" class="form-control" placeholder="输入关键词以查询" />'
			);
			$("#search-input").keypress(event => {
				if (event.keyCode === 13) search();
			});
		} else {
			$("aside > div").prepend(
				`<select class="show-tick form-control" id="select-attr-value" data-live-search="true" title="选择${queryBasis}"></select>`
			);
			let key = $("#select-query-basis")
				.find("option:selected")
				.html();
			$.get(`/all_detail?key=${key}`, data => {
				let oSelect = $("#select-attr-value");
				let toAddHTML = "";
				data.forEach(item => {
					toAddHTML += `<option>${item}</option>`;
				});
				oSelect.html(toAddHTML);
				oSelect.selectpicker();
			});
		}
	}, 1); // 让 modifySearchInputElement 事件在 bootstrap-select 指定的事件后面触发
}

function getCardHTML(item) {
	let aircraftImageHTML = "";
	let eventInfoHTML = "";
	if (item["客机型号"]) {
		aircraftImageHTML = `
			<img
				class="card-img-top"
				src="/static/aircrafts/${item["客机型号"].trim()}.jpeg"
				alt="${item["客机型号"].trim()}"
			/>`;
	}
	for (let i of ["时间", "出事地点", "航班号", "客机型号", "航空公司"]) {
		if (item[i])
			if (i == "时间")
				eventInfoHTML += `
					<div class="col-6">${i}：</div><div class="col-6">${item[i].slice(0, 4) +
					"/" +
					item[i].slice(4, 6) +
					"/" +
					item[i].slice(6)}</div>`;
			else
				eventInfoHTML += `<div class="col-6">${i}：</div><div class="col-6">${item[i]}</div>`;
	}
	return `
		<div class="card">
			${aircraftImageHTML}
			<div class="card-body text-center">
				<h2 class="card-title"><a class="text-success event-name" data-toggle="modal" data-target="#event-details">${item[
					"事件名"
				].slice(1)}</a></h2>
				<div class="card-text">
					<div class="row no-gutters">${eventInfoHTML}</div>
				</div>
				<div class="card-button">
					<button type="button" class="btn btn-outline-danger btn-sm delete-card-button" style="width: 40%">删除</button>
					<button type="button" class="btn btn-outline-success btn-sm modify-card-button" style="width: 40%" data-toggle="modal" data-target="#event-details">修改</button>
				</div>
			</div>
		</div>`;
}

function showAllEventCards(page, data) {
	// 显示所有事件卡片
	page = Number(page);
	let pageNum = data[data.length - 1]["page_num"];
	data.pop();

	let toAddHtml = "";
	const numPerRow = 3; // 每行的卡片个数
	let rowNum = Math.ceil(data.length / numPerRow);
	for (let i = 0; i < rowNum; i++) {
		toAddHtml += '<div class="card-columns">';
		for (let j = 0; j < numPerRow; j++)
			if (data[i * numPerRow + j])
				toAddHtml += getCardHTML(data[i * numPerRow + j]);
		toAddHtml += "</div>";
	}

	$("main>div").html(toAddHtml);
	$("a.event-name").on("click", showEventDetails);
	$(".delete-card-button").on("click", deleteCard);
	$(".modify-card-button").on("click", modifyCard);

	renderPager(page, pageNum, "/all_events_intro?page=", showAllEventCards);
}

function showSearchedEventCards(page, data, key, value) {
	// 以卡片的形式展示按条件搜索到的事件简介信息
	page = Number(page);
	let pageNum = data[data.length - 1]["page_num"];
	data.pop();

	let toAddHtml = "";
	const numPerRow = 3; // 每行的卡片个数
	let rowNum = Math.ceil(data.length / numPerRow);
	for (let i = 0; i < rowNum; i++) {
		toAddHtml += '<div class="card-columns">';
		for (let j = 0; j < numPerRow; j++)
			if (data[i * numPerRow + j])
				toAddHtml += getCardHTML(data[i * numPerRow + j]);
		toAddHtml += "</div>";
	}
	$("main>div").html(toAddHtml);
	$("a.event-name").on("click", showEventDetails);
	$(".delete-card-button").on("click", deleteCard);
	$(".modify-card-button").on("click", modifyCard);

	renderPager(
		page,
		pageNum,
		`/events_intro?key=${key}&value=${value}&page=`,
		showSearchedEventCards
	);
}

function renderPager(page, pageNum, url, clickCallback) {
	let showButtonNum; // 显示的分页按钮个数
	if (screen.availWidth >= 1200) showButtonNum = 15;
	else if (screen.availWidth <= 575) showButtonNum = 4;
	else showButtonNum = 9;
	if (pageNum <= showButtonNum) showButtonNum = pageNum;
	let pagerButtomHTML = (text, isActive, id = "") => {
		if (isActive)
			return `<li class="page-item active" id="${id}"><div class="page-link">${text}</div></li>`;
		else
			return `<li class="page-item" id="${id}"><div class="page-link">${text}</div></li>`;
	};
	let pagerMiddleButton = Math.ceil(showButtonNum * 0.5) + 1; // Math.ceil() 向上取整。为了更美观，加个一
	let middleLeftNum = pagerMiddleButton - 1;
	let middleRightNum = showButtonNum - pagerMiddleButton;

	let startButton, endButton, addEllipsis; // addEllipsis: 是否添加省略号。有三个值："front", "back", "both"
	if (page <= pagerMiddleButton) {
		startButton = 1;
		endButton = showButtonNum;
		addEllipsis = "back";
	} else if (page >= pageNum - middleRightNum) {
		startButton = pageNum - showButtonNum + 1;
		endButton = pageNum;
		addEllipsis = "front";
	} else {
		startButton = page - middleLeftNum;
		endButton = page + middleRightNum;
		addEllipsis = "both";
	}
	let toAddPager =
		pagerButtomHTML("<<", false, "pager-home") +
		pagerButtomHTML("<", false, "pager-previous");
	if (addEllipsis === "front" || addEllipsis === "both")
		toAddPager += pagerButtomHTML("...");
	for (let i = startButton; i <= endButton; i++) {
		if (page == i) toAddPager += pagerButtomHTML(i, true);
		else toAddPager += pagerButtomHTML(i);
	}
	if (addEllipsis === "back" || addEllipsis === "both")
		toAddPager += pagerButtomHTML("...");
	toAddPager +=
		pagerButtomHTML(">", false, "pager-next") +
		pagerButtomHTML(">>", false, "pager-end");

	$(".pager>ul").html(toAddPager);
	$(".pager li").on("click", obj => {
		if (
			[
				"<<",
				"<",
				">",
				">>",
				"...",
				"&lt;",
				"&lt;&lt;",
				"&gt;",
				"&gt;&gt;"
			].indexOf(obj.target.innerHTML) == -1
		) {
			$("main>div").html(getLoadingHTML("loading-events-card"));
			$(".pager>ul").html("");
			$.get(url + obj.target.innerHTML, data => {
				let key = /(?<=key=).*?(?=&)/.exec(url);
				let value = /(?<=value=).*?(?=&)/.exec(url);
				clickCallback(
					obj.target.innerHTML,
					data,
					key ? key : null,
					value ? value : null
				);
			});
		}
	});
	$(".pager .pager-previous").on("click", () => {
		if (page > 1) {
			$("main>div").html(getLoadingHTML("loading-events-card"));
			$(".pager>ul").html("");
			$.get(url + (page - 1), data => {
				clickCallback(
					page - 1,
					data,
					/(?<=key=).*?(?=&)/.exec(url)[0],
					/(?<=value=).*?(?=&)/.exec(url)[0]
				);
			});
		}
	});
	$(".pager .pager-next").on("click", () => {
		if (page < pageNum) {
			$("main>div").html(getLoadingHTML("loading-events-card"));
			$(".pager>ul").html("");
			$.get(url + (page + 1), data => {
				clickCallback(
					page + 1,
					data,
					/(?<=key=).*?(?=&)/.exec(url)[0],
					/(?<=value=).*?(?=&)/.exec(url)[0]
				);
			});
		}
	});
	$(".pager .pager-home").on("click", () => {
		if (page != 1) {
			$("main>div").html(getLoadingHTML("loading-events-card"));
			$(".pager>ul").html("");
			$.get(url + 1, data => {
				clickCallback(
					1,
					data,
					/(?<=key=).*?(?=&)/.exec(url)[0],
					/(?<=value=).*?(?=&)/.exec(url)[0]
				);
			});
		}
	});
	$(".pager .pager-end").on("click", () => {
		if (page != pageNum) {
			$("main>div").html(getLoadingHTML("loading-events-card"));
			$(".pager>ul").html("");
			$.get(url + pageNum, data => {
				clickCallback(
					pageNum,
					data,
					/(?<=key=).*?(?=&)/.exec(url)[0], // 只有 showSearchedEventCards 函数才会用到后面两个参数
					/(?<=value=).*?(?=&)/.exec(url)[0]
				);
			});
		}
	});
}

function showEventDetails(obj) {
	let title = obj.target.innerHTML;
	$("#event-details .modal-title").html(title);
	$("#event-details .modal-body").html(getLoadingHTML("loading-event-details"));
	$.get(`event_info?event_name=S${obj.target.innerHTML}`, data => {
		let toAddHTML =
			'<table class="table table-striped table-hover" id="eventDetailsTable"><tbody>';
		for (let i in data)
			toAddHTML += `<tr><th>${i}</th><td>${data[i]}</td></tr>`;
		toAddHTML += "</tbody></table>";
		$("#event-details .modal-body").html(toAddHTML);
	});
}

function modifyCard(obj) {
	let title =
		obj.target.parentElement.parentElement.firstElementChild.innerText;
	$("#event-details .modal-title").html(title);
	$("#event-details .modal-body").html(getLoadingHTML("loading-event-details"));
	$.get(`event_info?event_name=S${title}`, data => {
		let toAddHTML =
			'<table class="table table-striped table-hover" id="eventDetailsTable"><tbody>';
		for (let i in data)
			toAddHTML += `<tr><th>${i}</th><td><input type="text" class="form-control" value="${data[i]}"></td></tr>`;
		toAddHTML += "</tbody></table>";
		$("#event-details .modal-body").html(toAddHTML);
	});

	$("#event-details .modal-footer").html(`
		<button type="button" class="btn btn-secondary" data-dismiss="modal">关闭</button>
		<button type="button" class="btn btn-primary" onclick="sumbitCardData()">提交</button>
	`);
}

function deleteCard(obj) {
	let title =
		obj.target.parentElement.parentElement.firstElementChild.innerText;
	let data = {
		事件名: title
	};
	$.post("#", data, () => {});
}

function sumbitCardData() {
	let oTrs = $("#event-details .modal-body tr");
	let data = {};
	for (let tr of oTrs) {
		let key = tr.children[0].innerText;
		let value = tr.children[1].children[0].value;
		if (value == "") {
			console.log("不能为空");
			return;
		}
		data[key] = value;
	}
	$.post("#", data, () => {});
}

function addCard() {
	$("#event-details .modal-title").html("添加事件");
	$("#event-details .modal-body").html(getLoadingHTML("loading-event-details"));
	$.get(`pattern_bottom`, data => {
		let toAddHTML =
			'<table class="table table-striped table-hover" id="eventDetailsTable"><tbody>';
		toAddHTML += `<tr><th>事件名</th><td><input type="text" class="form-control"></td></tr>`;
		for (let i of data)
			toAddHTML += `<tr><th>${i}</th><td><input type="text" class="form-control"></td></tr>`;
		toAddHTML += "</tbody></table>";
		$("#event-details .modal-body").html(toAddHTML);
	});

	$("#event-details .modal-footer").html(`
		<button type="button" class="btn btn-secondary" data-dismiss="modal">关闭</button>
		<button type="button" class="btn btn-primary" onclick="sumbitCardData()">提交</button>
	`);
}

function searchNodes() {
	const ASIDE_WIDTH = $(".aside-panel").outerWidth();
	const NAVBAR_HEIGHT = $("#navbar").outerHeight();
	const WIDTH = screen.availWidth - ASIDE_WIDTH;
	const HEIGHT = screen.availHeight - NAVBAR_HEIGHT;

	let key = $("#select-query-basis")
		.find("option:selected")
		.html();
	let value = "";
	if (key === "时间")
		value = $("#search-input")
			.val()
			.split("/")
			.join("");
	else if (key === "原因" || key === "结果") value = $("#search-input").val();
	else
		value = $("#select-attr-value")
			.find("option:selected")
			.html();
	if (key && value) {
		let svg = $("#mainSvg");
		svg.remove();
		svg = createSvg(WIDTH, HEIGHT, true, "mainSvg");
		$("#mainSvg").attr(
			"transform",
			`translate(${ASIDE_WIDTH}, ${NAVBAR_HEIGHT})`
		);
		aForceDirectedGraph = forceDirectedGraph(svg)
			.json(`/one_event?key=${key}&value=${value}`)
			.render();
	}
}
