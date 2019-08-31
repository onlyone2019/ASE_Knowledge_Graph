function forceDirectedGraph(svg) {
	let _graph = {};
	let _nodeRadius = 30; // 最大结点半径(group 为 0 结点的半径)。其他结点会被缩放 1 - group / 10 倍。
	let _nodeSpacing = 1; // 结点间最小距离
	let _fontSize = 12; // 结点和链接文字大小
	let _jsonUrl;
	let _colorScale = d3.scaleOrdinal(d3.schemeSet3);

	/******** ↓ 获取或设置属性值 *********/

	_graph.nodeRadius = nr => {
		if (!nr) return _nodeRadius;
		_nodeRadius = nr;
		return _graph;
	};

	_graph.nodeSpacing = ns => {
		if (!ns) return _nodeSpacing;
		_nodeSpacing = ns;
		return _graph;
	};

	_graph.fontSize = fs => {
		if (!fs) return _fontSize;
		_fontSize = fs;
		return _graph;
	};

	_graph.json = ju => {
		if (!ju) return _jsonUrl;
		_jsonUrl = ju;
		return _graph;
	};

	_graph.colorScheme = cs => {
		_colorScale = d3.scaleOrdinal(cs);
		return _graph;
	};

	/******** ↑ 获取或设置属性值 *********/

	_graph.render = () => {
		let _simulation = d3
			.forceSimulation() // 创建力布局
			.alphaDecay(0.01) // alpha 衰减速度
			.force("charge", d3.forceManyBody().strength(-300)) // 多体力（多体力可以模拟引力和斥力）
			.force(
				"collision",
				d3.forceCollide(_nodeRadius + _nodeSpacing).strength(1)
			) // 碰撞力
			.force(
				"center",
				d3.forceCenter(svg.attr("width") / 2, svg.attr("height") / 2)
			); // 中心力

		d3.json(_jsonUrl).then(data => {
			_simulation.nodes(data.nodes);
			_simulation.force(
				"links",
				d3
					.forceLink(data.links)
					.strength(1)
					.distance(150)
					.id(d => d.index)
			); // 连接力
			_simulation.on("tick", ticked); // 监听 tick 事件

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

			nodeG.on("mouseenter", enterNodeG);

			nodeG.on("mouseleave", leaveNodeG);

			nodeG.on("click", function() {});

			nodeG.on("dbclick", function() {});

			/******** ↑ 监听各种事件 *********/

			/******** ↓ 事件处理程序 *********/

			function enterNodeG(d) {
				const G_ANGLE = Math.PI / 4; // g 元素的偏移角度
				const LINE1_WIDTH = _nodeRadius / 2; // 斜线的长度
				const LINE1_ANGLE = Math.PI / 4; // 斜线的水平偏角
				const LINE2_WIDTH = d.id.length * _fontSize + 15; // 直线的长度

				let gOffestX = Math.sin(G_ANGLE) * _nodeRadius; // g 元素在 X 方向上的偏移量
				let gOffestY = -(Math.cos(G_ANGLE) * _nodeRadius); // g 元素在 Y 方向上的偏移量
				let line1X = LINE1_WIDTH * Math.cos(LINE1_ANGLE); // 斜线在 X 方向上的长度
				let line1Y = LINE1_WIDTH * Math.sin(LINE1_ANGLE); // 斜线在 Y 方向上的长度

				let theNode = d3.select(this);
				let detailsG = theNode
					.append("g")
					.attr("transform", `translate(${gOffestX}, ${gOffestY})`)
					.classed("details", true);
				detailsG
					.append("line")
					.attr("x1", 0)
					.attr("y1", 0)
					.attr("x2", line1X)
					.attr("y2", -line1Y)
					.style("stroke", "black")
					.style("stroke-width", "1px");
				detailsG
					.append("line")
					.attr("x1", line1X)
					.attr("y1", -line1Y)
					.attr("x2", line1X + LINE2_WIDTH)
					.attr("y2", -line1Y)
					.style("stroke", "black")
					.style("stroke-width", "1px");
				detailsG
					.append("text")
					.attr("x", line1X + 7.5)
					.attr("y", -(line1Y + 3))
					.attr("font-size", _fontSize)
					.text(d.id);
			}

			function leaveNodeG() {
				d3.select(this)
					.select("g.details")
					.remove();
			}

			function ticked(e) {
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
			}

			function dragStarted(d) {
				if (!d3.event.active) _simulation.alphaTarget(0.3).restart();
				d.fx = d.x;
				d.fy = d.y;

				nodeG.on("mouseenter", null);
				d3.select(this)
					.select("g.details")
					.remove();
			}

			function dragged(d) {
				d.fx = d3.event.x;
				d.fy = d3.event.y;
			}

			function dragEnded(d) {
				if (!d3.event.active) _simulation.alphaTarget(0);
				d.fx = null;
				d.fy = null;

				nodeG.on("mouseenter", enterNodeG);
			}

			/******** ↑ 事件处理程序*********/
		});
	};

	return _graph;
}
