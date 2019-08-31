function lineChart(svg) {
	let _chart = {};
	let _margins = { top: 30, right: 30, bottom: 30, left: 30 };
	let _colorScale = d3.scaleOrdinal(d3.schemeCategory10);
	let _xScale = d3.scaleLinear();
	let _yScale = d3.scaleLinear();
	let _dotRadius = 3;
	let _jsonUrl;

	let _data = [];
	let _bodyG;
	let _line;

	_chart.render = function() {
		d3.json(_jsonUrl).then(data => {
			_xScale.domain([0, data[0].length - 1]); // 将第一个数据集的长度作为作用域
			_yScale.domain([0, data[0].length - 1]);
			data.forEach(dataset => {
				_data.push(
					d3.range(dataset.length).map(i => {
						return { x: i, y: dataset[i] };
					})
				);
			});

			renderAxes();
			defineBodyClip();
			renderBody();
		});
	};

	function renderAxes() {
		let axesG = svg.append("g");
		renderXAxis(axesG);
		renderYAxis(axesG);
	}

	function renderXAxis(axesG) {
		let xAxis = d3.axisBottom().scale(_xScale.range([0, quadrantWidth()]));

		axesG
			.append("g")
			.classed("x axis", true)
			.attr("transform", `translate(${xStart()}, ${yStart()})`)
			.call(xAxis);

		d3.selectAll("g.x g.tick")
			.append("line")
			.classed("grid-line", true)
			.attr("x1", 0)
			.attr("y1", 0)
			.attr("x2", 0)
			.attr("y2", -quadrantHeight());
	}

	function renderYAxis(axesG) {
		let yAxis = d3.axisLeft().scale(_yScale.range([quadrantHeight(), 0]));

		axesG
			.append("g")
			.classed("y axis", true)
			.attr("transform", `translate(${xStart()}, ${yEnd()})`)
			.call(yAxis);

		d3.selectAll("g.y g.tick")
			.append("line")
			.classed("grid-line", true)
			.attr("x1", 0)
			.attr("y1", 0)
			.attr("x2", quadrantWidth())
			.attr("y2", 0);
	}

	function defineBodyClip() {
		let padding = 5;

		svg
			.append("defs")
			.append("clipPath")
			.attr("id", "body-clip")
			.append("rect")
			.attr("x", 0 - padding)
			.attr("y", 0)
			.attr("width", quadrantWidth() + 2 * padding)
			.attr("height", quadrantHeight());
	}

	function renderBody() {
		_bodyG = svg
			.append("g")
			.attr("transform", `translate(${xStart()}, ${yEnd()})`)
			.attr("clip-path", "url(#body-clip)");

		renderLines();
		renderDots();
	}

	function renderLines() {
		_line = d3
			.line()
			.x(d => _xScale(d.x))
			.y(d => _yScale(d.y));

		let pathLines = _bodyG.selectAll("path.line").data(_data);

		pathLines
			.enter()
			.append("path")
			.merge(pathLines)
			.style("stroke", (d, i) => _colorScale(i))
			.classed("line", true)
			.attr("d", d => _line(d));
	}

	function renderDots() {
		_data.forEach((list, i) => {
			let circle = _bodyG.selectAll("circle._" + i).data(list);

			circle
				.enter()
				.append("circle")
				.merge(circle)
				.classed("dot", true)
				.style("stroke", () => _colorScale(i))
				.transition()
				.attr("cx", d => _xScale(d.x))
				.attr("cy", d => _yScale(d.y))
				.attr("r", _dotRadius);
		});
	}

	function xStart() {
		return _margins.left;
	}

	function yStart() {
		return svg.attr("height") - _margins.bottom;
	}

	function xEnd() {
		return svg.attr("width") - _margins.right;
	}

	function yEnd() {
		return _margins.top;
	}

	function quadrantWidth() {
		return svg.attr("width") - _margins.left - _margins.right;
	}

	function quadrantHeight() {
		return svg.attr("height") - _margins.top - _margins.bottom;
	}

	_chart.margins = (t, r, b, l) => {
		if (!arguments.length) return _margins;
		_margins = { top: t, right: r, bottom: b, left: l };
		return _chart;
	};

	_chart.dotRadius = dr => {
		if (!dr) return _dotRadius;
		_dotRadius = dr;
		return _chart;
	};

	_chart.json = ju => {
		if (!ju) return _jsonUrl;
		_jsonUrl = ju;
		return _chart;
	};

	_chart.colorScheme = cs => {
		_colorScale = d3.scaleOrdinal(cs);
		return _forceChart;
	};

	return _chart;
}
