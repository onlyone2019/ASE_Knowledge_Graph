function createSvg(width, height, parent) {
	if (!parent) parent = "body";
	return d3
		.select(parent)
		.append("svg")
		.attr("width", width)
		.attr("height", height);
}

function forceDirectedGraph(svg) {
	let _forceChart = {};
	let _nodeRadius = 30; // 最大结点半径(group 为 0 结点的半径)。其他结点会被缩放 1 - group / 10 倍。
	let _nodeSpacing = 1; // 结点间最小距离
	let _fontSize = 12; // 结点和链接文字大小
	let _jsonUrl;
	let _colorScale = d3.scaleOrdinal(d3.schemeSet3);

	/******** ↓ 获取或设置属性值 *********/

	_forceChart.nodeRadius = nr => {
		if (!nr) return _nodeRadius;
		_nodeRadius = nr;
		return _forceChart;
	};

	_forceChart.nodeSpacing = ns => {
		if (!ns) return _nodeSpacing;
		_nodeSpacing = ns;
		return _forceChart;
	};

	_forceChart.fontSize = fs => {
		if (!fs) return _fontSize;
		_fontSize = fs;
		return _forceChart;
	};

	_forceChart.json = ju => {
		if (!ju) return _jsonUrl;
		_jsonUrl = ju;
		return _forceChart;
	};

	_forceChart.colorScheme = cs => {
		_colorScale = d3.scaleOrdinal(cs);
		return _forceChart;
	};

	/******** ↑ 获取或设置属性值 *********/

	_forceChart.render = () => {
		/******** ↓ 拖曳事件回调函数 *********/

		function dragStarted(d) {
			if (!d3.event.active) _simulation.alphaTarget(1).restart();
			d.fx = d.x;
			d.fy = d.y;
		}

		function dragged(d) {
			d.fx = d3.event.x;
			d.fy = d3.event.y;
		}

		function dragEnded(d) {
			if (!d3.event.active) _simulation.alphaTarget(0);
			d.fx = null;
			d.fy = null;
		}

		/******** ↑ 拖曳事件回调函数 *********/

		/******** ↓ 创建力布局 *********/

		let _simulation = d3
			.forceSimulation()
			.force("charge", d3.forceManyBody())
			.force(
				"collision",
				d3.forceCollide(_nodeRadius + _nodeSpacing).strength(1)
			)
			.force(
				"center",
				d3.forceCenter(svg.attr("width") / 2, svg.attr("height") / 2)
			);

		/******** ↑ 创建力布局 *********/

		d3.json(_jsonUrl).then(data => {
			_simulation.nodes(data.nodes);
			_simulation.force(
				"links",
				d3
					.forceLink(data.links)
					.strength(1)
					.distance(200)
					.id(d => d.index)
			);
			_simulation.on("tick", e => {
				link
					.attr("x1", d => d.source.x)
					.attr("y1", d => d.source.y)
					.attr("x2", d => d.target.x)
					.attr("y2", d => d.target.y);
				linkText
					.attr("x", d => (d.source.x + d.target.x) / 2)
					.attr("y", d => (d.source.y + d.target.y) / 2);

				nodeG.attr(
					"transform",
					d => `translate(${d.x}, ${d.y}) scale(${1 - d.group / 10})`
				);
			});

			/******** ↓ 创建组成力导向图的元素 *********/

			let link = svg
				.append("g")
				.selectAll("line")
				.data(data.links)
				.enter()
				.append("line")
				.style("stroke", "#999")
				.style("stroke-width", "1px");

			let linkText = svg
				.append("g")
				.selectAll("text")
				.data(data.links)
				.enter()
				.append("text")
				.text(d => d.linkText)
				.style("font-size", _fontSize);

			let nodeG = svg
				.append("g")
				.selectAll("g")
				.data(data.nodes)
				.enter()
				.append("g")
				.style("cursor", "pointer")
				.call(
					d3
						.drag() // <-G
						.on("start", dragStarted)
						.on("drag", dragged)
						.on("end", dragEnded)
				);

			nodeG
				.append("circle")
				.attr("r", _nodeRadius)
				.style("fill", d => _colorScale(d.group))
				.style("stroke", "gray");

			nodeG
				.append("text")
				.text(d => {
					let canShow = Math.floor((_nodeRadius * 2 - 4) / _fontSize); // circle 能容纳的字数
					if (d.id.length > canShow) return d.id.slice(0, canShow - 1) + "...";
					else return d.id;
				})
				.attr("font-size", _fontSize)
				.attr("fill", "black")
				.attr("x", d => {
					let canShow = Math.floor((_nodeRadius * 2 - 4) / _fontSize);
					if (d.id.length > canShow) return -(canShow * _fontSize) / 2;
					else return -(d.id.length * _fontSize) / 2;
				})
				.attr("y", (_fontSize - 4) / 2);

			/******** ↑ 创建组成力导向图的元素 *********/

			/******** ↓ 监听各种事件 *********/

			nodeG.on("mouseenter", function() {});

			nodeG.on("mouseleave", function() {});

			nodeG.on("click", function() {});

			nodeG.on("dbclick", function() {});

			/******** ↑ 监听各种事件 *********/
		});
	};

	return _forceChart;
}
