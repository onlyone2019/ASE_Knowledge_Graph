function goToTop() {
	window.scroll(0, 0);
}

function getLoadingHTML(id) {
	return `
		<div id="${id}">
			<div class="spinner-border text-warning" role="status"></div>
			<span>Loading...</span>
		</div>`;
}

function getCardHTML(item) {
	let eventInfoHTML = "";
	for (let i of ["日期", "出事地点", "航班号", "客机型号", "航空公司"]) {
		if (item[i])
			if (i == "日期")
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
			<img
				class="card-img-top"
				src="/static/aircrafts/${item["客机型号"]}.jpeg"
				alt="${item["客机型号"]}"
			/>
			<div class="card-body text-center">
				<h2 class="card-title"><a class="text-success event-name" data-toggle="modal" data-target="#event-details">${
					item["事件名"]
				}</a></h2>
				<div class="card-text">
					<div class="row no-gutters">${eventInfoHTML}</div>
				</div>
			</div>
		</div>`;
}

function showAllEventCards(page, data) {
	// 显示所有事件卡片（后端分页）
	page = Number(page);
	let jsonArray = JSON.parse(data);
	let pageNum = jsonArray[jsonArray.length - 1]["page_num"];
	jsonArray.pop();
	let toAddHtml = "";
	jsonArray.forEach(item => {
		toAddHtml += getCardHTML(item);
	});
	$("main>div").html(toAddHtml);
	$("a.event-name").on("click", showEventDetails);

	let showButtonNum = 15; // 显示的分页按钮个数
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
		pagerButtomHTML("Home", false, "pager-home") +
		pagerButtomHTML("Prev", false, "pager-previous");
	if (addEllipsis === "front" || addEllipsis === "both")
		toAddPager += pagerButtomHTML("...");
	for (let i = startButton; i <= endButton; i++) {
		if (page == i) toAddPager += pagerButtomHTML(i, true);
		else toAddPager += pagerButtomHTML(i);
	}
	if (addEllipsis === "back" || addEllipsis === "both")
		toAddPager += pagerButtomHTML("...");
	toAddPager +=
		pagerButtomHTML("Next", false, "pager-next") +
		pagerButtomHTML("End", false, "pager-end");

	$("#pager>ul").html(toAddPager);
	$("#pager li").on("click", obj => {
		if (
			["Home", "Previous", "Next", "End", "..."].indexOf(
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
	// 不分页
	let jsonArray = JSON.parse(data);
	let toAddHtml = "";
	jsonArray.forEach(item => {
		toAddHtml += getCardHTML(item);
	});
	$("main>div").html(toAddHtml);
	$("a.event-name").on("click", showEventDetails);
}

function showEventDetails(obj) {
	let title = obj.target.innerHTML;
	$("#event-details .modal-title").html(title);
	$("#event-details .modal-body").html(getLoadingHTML("loading-event-details"));
	$.get(`event_info?event_name=${obj.target.innerHTML}`, data => {
		let jsonObj = JSON.parse(data);
		let toAddHTML = '<table class="table table-striped table-hover"><tbody>';
		for (let i in jsonObj)
			toAddHTML += `<tr><th>${i}</th><td>${jsonObj[i]}</td></tr>`;
		toAddHTML += "</tbody></table>";
		$("#event-details .modal-body").html(toAddHTML);
	});
}
