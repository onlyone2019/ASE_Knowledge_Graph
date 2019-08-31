function createSvg(width, height, canZoom = false, parent = "body") {
	let svg = d3
		.select(parent)
		.append("svg")
		.attr("width", width)
		.attr("height", height);

	if (canZoom) {
		let g = svg
			.append("g")
			.attr("transform", `translate(${width / 2}, ${height / 2})`);
		svg.call(
			d3
				.zoom()
				.scaleExtent([0.2, 5])
				.on("zoom", () => {
					let transform = d3.event.transform;
					g.attr(
						"transform",
						`translate(${transform.x + width / 2}, ${transform.y +
							height / 2})scale(${transform.k})`
					);
				})
		);
		return g;
	} else return svg;
}

// 统计字符串包含的字符个数，汉字算两个字符
function calcCharNum(string) {
	let charNum = 0;
	if (!string) return 0;
	for (let i = 0; i < string.length; i++)
		charNum += string.charCodeAt(i) > 255 ? 2 : 1;
	return charNum;
}
