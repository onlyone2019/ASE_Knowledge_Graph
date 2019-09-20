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
