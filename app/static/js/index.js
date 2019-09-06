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
				<h2 class="card-title"><a class="text-success event-name" data-toggle="modal" data-target="#event-details">${
					item["事件名"].slice(1)
				}</a></h2>
				<div class="card-text">
					<div class="row no-gutters">${eventInfoHTML}</div>
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
	data.forEach(item => {
		toAddHtml += getCardHTML(item);
	});
	$("main>div").html(toAddHtml);
	$("a.event-name").on("click", showEventDetails);

	let showButtonNum; // 显示的分页按钮个数
	if (screen.availWidth >= 1200)
		showButtonNum = 15;
	else if (screen.availWidth <= 600)
		showButtonNum = 4;
	else
		showButtonNum = 9
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

	$("#pager>ul").html(toAddPager);
	$("#pager li").on("click", obj => {
		if (
			["<<", "<", ">", ">>", "..."].indexOf(
				obj.target.innerHTML
			) == -1
		) {
			$("main>div").html(getLoadingHTML("loading-events-card"));
			$("#pager>ul").html("");
			$.get(`/all_events_intro?page=${obj.target.innerHTML}`, data => {
				showAllEventCards(obj.target.innerHTML, data);
			});
		}
	});
	$("#pager #pager-previous").on("click", () => {
		if (page > 1) {
			$("main>div").html(getLoadingHTML("loading-events-card"));
			$("#pager>ul").html("");
			$.get(`/all_events_intro?page=${page - 1}`, data => {
				showAllEventCards(page - 1, data);
			});
		}
	});
	$("#pager #pager-next").on("click", () => {
		if (page < pageNum) {
			$("main>div").html(getLoadingHTML("loading-events-card"));
			$("#pager>ul").html("");
			$.get(`/all_events_intro?page=${page + 1}`, data => {
				showAllEventCards(page + 1, data);
			});
		}
	});
	$("#pager #pager-home").on("click", () => {
		if (page != 1) {
			$("main>div").html(getLoadingHTML("loading-events-card"));
			$("#pager>ul").html("");
			$.get(`/all_events_intro?page=${1}`, data => {
				showAllEventCards(1, data);
			});
		}
	});
	$("#pager #pager-end").on("click", () => {
		if (page != pageNum) {
			$("main>div").html(getLoadingHTML("loading-events-card"));
			$("#pager>ul").html("");
			$.get(`/all_events_intro?page=${pageNum}`, data => {
				showAllEventCards(pageNum, data);
			});
		}
	});
}

function showSearchedEventCards(data) {
	// 以卡片的形式展示按条件搜索到的事件简介信息
	data.pop();
	let toAddHtml = "";
	data.forEach(item => {
		toAddHtml += getCardHTML(item);
	});
	$("main>div").html(toAddHtml);
	$("a.event-name").on("click", showEventDetails);
}

function showEventDetails(obj) {
	let title = obj.target.innerHTML;
	$("#event-details .modal-title").html(title);
	$("#event-details .modal-body").html(getLoadingHTML("loading-event-details"));
	$.get(`event_info?event_name=S${obj.target.innerHTML}`, data => {
		let toAddHTML = '<table class="table table-striped table-hover"><tbody>';
		for (let i in data)
			toAddHTML += `<tr><th>${i}</th><td>${data[i]}</td></tr>`;
		toAddHTML += "</tbody></table>";
		$("#event-details .modal-body").html(toAddHTML);
	});
}
