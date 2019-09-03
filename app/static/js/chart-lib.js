function createSvg(width, height, canZoom = false, parent = "body") {
	let svg = d3
		.select(parent)
		.append("svg")
		.attr("width", width)
		.attr("height", height);

	if (canZoom) {
		let g = svg.append("g");
		let zoom = d3
			.zoom()
			.scaleExtent([0.2, 5])
			.on("zoom", () => {
				g.attr("transform", d3.event.transform);
			});
		svg.call(zoom).on("dblclick.zoom", null); // 删除 svg 的双击缩放事件
		svg.call(zoom.transform, d3.zoomIdentity.translate(width / 2, height / 2));
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
