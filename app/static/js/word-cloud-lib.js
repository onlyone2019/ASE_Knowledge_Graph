// 需要 https://cdn.bootcss.com/d3-cloud/1.2.5/d3.layout.cloud.min.js
function wordCloud(svg) {
	let _wordCloud = {};
	let _jsonUrl;
	let _colorScale = d3.scaleOrdinal(d3.schemeCategory10);
	let _rotateArray = [-60, -30, 0, 30, 60]; // 旋转角度集合
	let _maxFontSize = 120; // 最大字体大小。最好不要超过 120，不要设太大，不然有些字符会消失

	_wordCloud.json = ju => {
		if (!ju) return _jsonUrl;
		_jsonUrl = ju;
		return _wordCloud;
	};

	_wordCloud.colorScheme = cs => {
		_colorScale = d3.scaleOrdinal(cs);
		return _wordCloud;
	};

	_wordCloud.rotateArray = ra => {
		if (!ra) return _rotateArray;
		_rotateArray = ra;
		return _wordCloud;
	};

	_wordCloud.maxFontSize = ms => {
		if (!ms) return _maxFontSize;
		_maxFontSize = ms;
		return _wordCloud;
	};

	_wordCloud.render = () => {
		d3.json(_jsonUrl).then(data => {
			let maxSize = 0;
			for (let item of data) // 找 data 中的最大 size
				if (item.size > maxSize) maxSize = item.size;
			let mapValue = maxSize / _maxFontSize; // 求出映射值

			d3.layout
				.cloud()
				.size([svg.attr("width"), svg.attr("height")])
				.words(data)
				.rotate(
					d => _rotateArray[Math.floor(Math.random() * _rotateArray.length)]
				)
				.fontSize(d => d.size / mapValue)
				.spiral("archimedean")
				.on("end", draw)
				.start();
		});
	};

	function draw(words) {
		svg
			.classed("word-cloud", true)
			.append("g")
			.attr(
				"transform",
				`translate(${svg.attr("width") / 2},${svg.attr("height") / 2})`
			)
			.selectAll("text")
			.data(words)
			.enter()
			.append("text")
			.style("font-size", 0)
			.style("text-anchor", "middle")
			.transition()
			.duration(500)
			.style("font-size", d => d.size + "px")
			.style("fill", (d, i) => _colorScale(i))
			.attr("transform", d => `translate(${[d.x, d.y]})rotate(${d.rotate})`)
			.text(d => d.text);
	}

	return _wordCloud;
}
