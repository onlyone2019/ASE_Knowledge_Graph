function goToTop() {
	window.scroll(0, 0);
}

function getLoadingHTML() {
	return `
		<div id="loading">
			<div class="spinner-border text-warning" role="status"></div>
			<span>Loading...</span>
		</div>`
}

function showEventsCard(page, data) {
	let jsonArray = JSON.parse(data);
	let page_num = jsonArray[jsonArray.length - 1]['page_num'];
	delete jsonArray[jsonArray.length - 1];
	jsonArray.length = jsonArray.length - 1;
	let toAddHtml = "";
	for (let item of jsonArray)
		toAddHtml +=
			`<div class="card">
				<img
					class="card-img-top"
					src="/static/images/test-picture.jpg"
					alt="${item['客机型号']}"
				/>
				<div class="card-body text-center">
					<h2 class="card-title"><a href="#" class="text-success">${item["事件名"]}</a></h2>
					<div class="card-text">
						<div class="row no-gutters">
							<div class="col-6">日期：</div>
							<div class="col-6">${item["日期"]}</div>
							<div class="col-6">出事地点：</div>
							<div class="col-6">${item["出事地点"]}</div>
							<div class="col-6">航班号：</div>
							<div class="col-6">${item["航班号"]}</div>
							<div class="col-6">客机型号：</div>
							<div class="col-6">${item["客机型号"]}</div>
							<div class="col-6">航空公司：</div>
							<div class="col-6">${item["航空公司"]}</div>
						</div>
					</div>
				</div>
			</div>`
	$("main>div").html(toAddHtml);

	const PAGER_BUTTON_NUM = 15
	let toAddPager = '<li class="page-item"><div class="page-link">&laquo;</div></li>'
	let show_num = 0;
	if (page_num <= PAGER_BUTTON_NUM)
		show_num = page_num;
	else
		show_num = PAGER_BUTTON_NUM;
	for (let i = 1; i <= show_num; i++) {
		if (page == i)
			toAddPager += `<li class="page-item active"><div class="page-link">${i}</div></li>`;
		else
			toAddPager += `<li class="page-item"><div class="page-link">${i}</div></li>`;
	}
	if (page_num > PAGER_BUTTON_NUM)
		toAddPager += '<li class="page-item"><div class="page-link">...</div></li>'
	toAddPager += '<li class="page-item"><div class="page-link">&raquo;</div></li>'
	$("#pager>ul").html(toAddPager);
	$("#pager li").on('click', obj => {
		if (obj.target.innerHTML == '«' || obj.target.innerHTML == '»' || obj.target.innerHTML == '...')
			return;
		$('main>div').html(getLoadingHTML);
		$.get(`/all_events_intro?page=${obj.target.innerHTML}`, (data) => { showEventsCard(obj.target.innerHTML, data) });
	})
	$("#pager li:first-child").on('click', () => {
		if (page > 1) {
			$('main>div').html(getLoadingHTML);
			$.get(`/all_events_intro?page=${Number(page) - 1}`, (data) => { showEventsCard(Number(page) - 1, data) });
		}
	})
	$("#pager li:last-child").on('click', () => {
		if (page < page_num) {
			$('main>div').html(getLoadingHTML);
			$.get(`/all_events_intro?page=${Number(page) + 1}`, (data) => { showEventsCard(Number(page) + 1, data) });
		}
	})
}
