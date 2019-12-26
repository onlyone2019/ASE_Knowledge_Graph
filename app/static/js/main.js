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
