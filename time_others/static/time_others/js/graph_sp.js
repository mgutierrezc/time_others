/*
Principal maintainer: Rachel Chen <me@rachelchen.me>
Contributors:
    Eli Pandolfo, epandolf@ucsc.edu
*/

// creates a new Vue app, that holds all information related to the graph
var vm = new Vue({
    components: {
      rangeSlider: RangeSlider,
    },
    el: "#app",
    data: function () {
      // returns an object containing all initial values for the graph's data
      // all properties in data are globally available to the html document
      return Object.assign(
        {
          // DO NOT CHANGE THE FOLLOWING
          circleRadius: 8,
          squareLength: 16, // this must be the multiple of 2 of circleRadius
          radius: {
            a: 0,
            b: 100,
          },
          graph: {
            currentLength: 0,
            svg: null,
            x: null,
            xAxis: null,
            y: null,
            yAxis: null,
            line: null,
            minX: 0,
            maxX: 0,
            minY: 0,
            maxY: 0,
          },
          tip: [],
          minMax: [],
          graphData: [],
          selected: [
            {
              x: null,
              y: null,
            },
            {
              x: null,
              y: null,
            },
          ],
          equations: [],
          once: false,
          fixed: {},
        },
        appSpecific
      );
    },
    // computes graph dimensions based on size of browser
    computed: {
      dimension: function () {
        //console.log(this.width - this.margin.left - this.margin.right)
        //console.log(this.height - this.margin.top - this.margin.bottom)
        return {
          width: this.width - this.margin.left - this.margin.right,
          height: this.height - this.margin.top - this.margin.bottom,
        };
      },
    },
    // object that watches for changes and then changes properties accordingly
    watch: {
      "prob.a": function (val, old) {
        if (this.once !== false && typeof this.onChangeCallback === "function")
          this.onChangeCallback();
  
        this.once = true; // invalidated changes on initialization
  
        this.prob.b = this.constants.maxArea - val;
  
        var areaA = this.constants.k * val;
        var areaB = this.constants.k * this.prob.b;
  
        this.radius.a = Math.pow(areaA / Math.PI, 1);
        this.radius.b = Math.pow(areaB / Math.PI, 1);
  
        d3.select('[line-index="a"]').attr("r", this.radius.a);
        d3.select('[line-index="b"]').attr("r", this.radius.b);
  
        this.tip.a.text(null);
        this.tip.a
          .append("tspan")
          .attr("x", this.tip.a.attr("x"))
          .attr("dx", this.equation.a.x > 50 ? "-150px" : "0px")
          .text("Estado A: " + this.prob.a.toFixed(0) + "% posible");
        this.tip.a
          .append("tspan")
          .attr("x", this.tip.a.attr("x"))
          .attr("dy", "15px")
          .attr("dx", this.equation.a.x > 50 ? "-150px" : "0px")
          .text("Tú: " + this.equation.a.x);
        this.tip.a
          .append("tspan")
          .attr("x", this.tip.a.attr("x"))
          .attr("dy", "15px")
          .attr("dx", this.equation.a.x > 50 ? "-150px" : "0px")
          .text("Pareja: " + this.equation.a.y);
  
        this.tip.b.text(null);
        this.tip.b
          .append("tspan")
          .attr("x", this.tip.b.attr("x"))
          .attr("dx", this.equation.b.x > 50 ? "-150px" : "0px")
          .text("Estado B: " + this.prob.b.toFixed(0) + "% posible");
        this.tip.b
          .append("tspan")
          .attr("x", this.tip.b.attr("x"))
          .attr("dy", "15px")
          .attr("dx", this.equation.b.x > 50 ? "-150px" : "0px")
          .text("Tú: " + this.equation.b.x);
        this.tip.b
          .append("tspan")
          .attr("x", this.tip.b.attr("x"))
          .attr("dy", "15px")
          .attr("dx", this.equation.b.x > 50 ? "-150px" : "0px")
          .text("Pareja: " + this.equation.b.y);
      },
    },
    methods: {
      fn: function (index, x) {
        // m = px * x + py * y
        // so, solve for y , y = m/py - px/py * x
        if (this.mode === "probability") {
          return this.equation.a.x === x ? this.equation.a.y : this.equation.b.y;
        } else {
          return (
            this.equations[index].m / this.equations[index].py -
            (this.equations[index].px / this.equations[index].py) * x
          );
        }
      },
      fnInverse: function (index, y) {
        if (this.mode === "probability") {
          return this.equation.a.y === y ? this.equation.a.x : this.equation.b.x;
        } else {
          return (
            this.equations[index].m / this.equations[index].px -
            (this.equations[index].py / this.equations[index].px) * y
          );
        }
      },
      // plots the utility function with step size
      plots: function () {
        if (this.mode === "probability") {
          var points = [];
          points.push(this.equation.a);
          points.push(this.equation.b);
          this.graphData.push(points);
          return;
        }
        for (var index = 0; index < this.equations.length; index++) {
          this.graphData[index] = [];
          this.graphData[index].push({
            x: 0,
            y: this.fn(index, 0),
          });
          this.graphData[index].push({
            x: this.fnInverse(index, 0),
            y: 0,
          });
        }
      },
  
      // d3.js
      reset: function () {
        this.equations = [];
        this.tip = [];
        this.minMax = [];
        this.graphData = [];
        this.selected = [
          {
            x: null,
            y: null,
          },
          {
            x: null,
            y: null,
          },
        ];
        this.equations = [];
      },
      sanity: function () {
        switch (this.mode) {
          case "single":
          case "single_given":
            this.equations.push(this.equation);
            break;
          case "probability":
            this.equations = [];
            this.equations.push({
              m: 0,
              py: 0,
              px: 0,
            });
            break;
          case "single_fixedsquare":
            this.equations.push({
              m: this.fixed.m,
              py: this.fixed.py,
              px: this.fixed.px,
            });
            this.equations.push(this.equation);
            break;
          case "single_fixedcircle":
            this.equations.push(this.equation);
            this.equations.push({
              m: this.fixed.m,
              py: this.fixed.py,
              px: this.fixed.px,
            });
            break;
        case "independent":
        case "newone":
            this.equations.push(this.equation);
            this.equations.push({
                m: this.equations[0].m,
                py: this.equations[0].py,
                px: this.equations[0].px,
                m: this.equations[0].m2,
                py: this.equations[0].py2,
                px: this.equations[0].px2,
            });
            break;
          case "positive":
            this.equations.push(this.equation);
            this.equations.push({
              m: this.equations[0].m,
              py: this.equations[0].py,
              px: this.equations[0].px,
            });
            break;
          case "negative": {
            this.equations.push(this.equation);
            this.equations.push({
              m: this.equations[0].m,
              py: this.equations[0].px,
              px: this.equations[0].py,
            });
            break;
          }
          default:
            break;
        }
      },
      init: function () {
        var self = this;
  
        this.graph.svg = d3
          .select(".graph")
          .append("svg")
          .attr(
            "width",
            this.dimension.width + this.margin.left + this.margin.right
          )
          .attr(
            "height",
            this.dimension.height + this.margin.top + this.margin.bottom
          )
          .append("g")
          .attr(
            "transform",
            "translate(" + this.margin.left + "," + this.margin.top + ")"
          );
  
        var length = 0;
  
        if (this.mode === "probability") {
          length = 1;
        } else {
          length = this.equations.length;
        }
  
        this.graph.x = d3.scaleLinear().range([0, this.dimension.width]);
  
        this.graph.y = d3.scaleLinear().range([this.dimension.height, 0]);
  
        this.graph.line = d3
          .line()
          .x(function (d) {
            return self.graph.x(d.x);
          })
          .y(function (d) {
            return self.graph.y(d.y);
          });
  
        this.graph.minX = Math.min.apply(
          null,
          this.graphData.map(function (d) {
            return Math.min.apply(
              null,
              d.map(function (c) {
                return c.x;
              })
            );
          })
        );
        this.graph.maxX = Math.max.apply(
          null,
          this.graphData.map(function (d) {
            return Math.max.apply(
              null,
              d.map(function (c) {
                return c.x;
              })
            );
          })
        );
        this.graph.minY = Math.min.apply(
          null,
          this.graphData.map(function (d) {
            return Math.min.apply(
              null,
              d.map(function (c) {
                return c.y;
              })
            );
          })
        );
        this.graph.maxY = Math.max.apply(
          null,
          this.graphData.map(function (d) {
            return Math.max.apply(
              null,
              d.map(function (c) {
                return c.y;
              })
            );
          })
        );
  
        for (var i = 0; i < this.equations.length; i++) {
          this.minMax[i] = {};
          this.minMax[i].minX = Math.min.apply(
            null,
            this.graphData[i].map(function (d) {
              return d.x;
            })
          );
          this.minMax[i].maxX = Math.max.apply(
            null,
            this.graphData[i].map(function (d) {
              return d.x;
            })
          );
          this.minMax[i].minY = Math.min.apply(
            null,
            this.graphData[i].map(function (d) {
              return d.y;
            })
          );
          this.minMax[i].maxY = Math.max.apply(
            null,
            this.graphData[i].map(function (d) {
              return d.y;
            })
          );
        }
      },
      drawAxis: function () {
        if (this.scale.type === "dynamic") {
          this.graph.x.domain([0, this.graph.maxX]);
          this.graph.y.domain([0, this.graph.maxY]);
        } else {
          this.graph.x.domain([0, this.scale.max]);
          this.graph.y.domain([0, this.scale.max]);
        }
  
        var tickStep = 10;
        var xTicks = [],
          x = 0,
          yTicks = [],
          y = 0;
        do {
          xTicks.push(x);
          x += tickStep;
        } while (
          x <= (this.scale.type === "fixed" ? this.scale.max : this.graph.maxX)
        );
  
        do {
          yTicks.push(y);
          y += tickStep;
        } while (
          y <= (this.scale.type === "fixed" ? this.scale.max : this.graph.maxY)
        );
  
        for (var i = 0; i < xTicks.length; i++) {
          this.graph.svg
            .append("path")
            .style("stroke", "#f2f2f2")
            .attr(
              "d",
              this.graph.line([
                { x: xTicks[i], y: 0 },
                {
                  x: xTicks[i],
                  y:
                    this.scale.type === "fixed"
                      ? this.scale.max
                      : this.graph.maxY,
                },
              ])
            );
  
          this.graph.svg
            .append("path")
            .style("stroke", "#f2f2f2")
            .attr(
              "d",
              this.graph.line([
                { x: 0, y: yTicks[i] },
                {
                  x:
                    this.scale.type === "fixed"
                      ? this.scale.max
                      : this.graph.maxX,
                  y: yTicks[i],
                },
              ])
            );
        }
  
        this.graph.xAxis = d3
          .axisBottom(this.graph.x)
          .tickValues(xTicks)
          .tickSize(6);
        this.graph.yAxis = d3
          .axisLeft(this.graph.y)
          .tickValues(yTicks)
          .tickSize(6);
  
        this.graph.svg
          .append("g")
          .attr("class", "gray")
          .attr("transform", "translate(0, " + this.dimension.height + ")")
          .call(this.graph.xAxis);
  
        this.graph.svg
          .append("text")
          .attr(
            "transform",
            "translate(" +
              this.dimension.width / 2 +
              ", " +
              (this.dimension.height + this.margin.top + 15) +
              ")"
          )
          .style("text-anchor", "middle")
          .text(this.label.x);
  
        this.graph.svg.append("g").attr("class", "gray").call(this.graph.yAxis);
  
        this.graph.svg
          .append("text")
          .attr("transform", "rotate(-90)")
          .attr("y", 0 - this.margin.left)
          .attr("x", 0 - this.dimension.height / 2)
          .attr("dy", "1em")
          .style("text-anchor", "middle")
          .text(this.label.y);
      },
      // draw the equation with d3.js
      draw: function () {
        var self = this;
  
        if (this.scale.type === "dynamic") {
          this.graph.x.domain([0, this.graph.maxX]);
          this.graph.y.domain([0, this.graph.maxY]);
        } else {
          this.graph.x.domain([0, this.scale.max]);
          this.graph.y.domain([0, this.scale.max]);
        }
  
        var color = "MediumPurple";
  
        if (this.mode === "probability") color = "PaleGreen";
  
        for (var index = 0; index < this.equations.length; index++) {
          this.graph.svg
            .append("path")
            .style(
              "stroke",
              (index === 0 && this.mode === "single_fixedsquare") ||
                (index === 1 && this.mode === "single_fixedcircle")
                ? "white"
                : color
            )
            .attr("d", this.graph.line(this.graphData[index]));
        }
      },
      showSelect: function () {
        var self = this;
  
        var randomX;
  
        var length = 0;
  
        if (this.mode === "probability") {
          length = 1;
        } else {
          length = this.equations.length;
        }
  
        for (var index = 0; index < length; index++) {
          if (this.mode === "probability") {
            randomX = this.equation.a.x;
          } else {
            if (index === 0) {
              if (this.mode === "single_fixedsquare") {
                randomX = this.fixed.x;
              } else {
                randomX =
                  Math.random() *
                    (this.minMax[index].maxX - this.minMax[index].minX) +
                  this.minMax[index].minX;
              }
            } else {
              if (this.mode === "single_fixedcircle") {
                randomX = this.fixed.x;
              } else if (this.mode === "single_fixedsquare") {
                randomX =
                  Math.random() *
                    (this.minMax[index].maxX - this.minMax[index].minX) +
                  this.minMax[index].minX;
              } else if (this.mode !== "positive") {
                var currentXValue = self.fnInverse(index, randomX);
                if (currentXValue > self.minMax[index].maxX)
                  currentXValue = self.minMax[index].maxX;
                if (currentXValue < self.minMax[index].minX)
                  currentXValue = self.minMax[index].minX;
                randomX = currentXValue;
              }
            }
  
            this.$set(this.selected, index, {
              x: null,
              y: null,
            });
  
            this.selected[index].x = randomX.toFixed(this.precision);
            this.selected[index].y = self
              .fn(index, randomX)
              .toFixed(this.precision);
  
            var text = "";
  
            if (
              [
                "independent",
                "single",
                "negative",
                "single_fixedsquare",
                "single_fixedcircle",
                "newone",
              ].indexOf(self.mode) !== -1
            ) {
              if (index === 0) {
                text =
                  "Tú (A: " +
                  self.selected[index].x +
                  ", B: " +
                  self.selected[index].y +
                  ")";
              } else {
                text =
                  "Pareja (A: " +
                  self.selected[index].x +
                  ", B: " +
                  self.selected[index].y +
                  ")";
              }
            } else if (self.mode === "single_given") {
              text =
                "Tú: " +
                self.selected[index].x +
                ", Pareja: " +
                self.selected[index].y;
            } else if (self.mode === "positive") {
              text =
                "Tú = Pareja (A: " +
                self.selected[index].x +
                ", B: " +
                self.selected[index].y +
                ")";
            }
  
            self.tip[index] = this.graph.svg
              .append("text")
              .attr("x", self.graph.x(randomX) + 15)
              .attr("y", self.graph.y(self.fn(index, randomX)) - 15)
              .text(text);
          }
  
          var drag = d3.drag().on("drag", function (d) {
            if (typeof self.onChangeCallback === "function")
              self.onChangeCallback();
  
            var me = d3.select(this);
            var index = me.attr("line-index");
  
            var xValue = self.graph.x.invert(d3.event.x);
            if (xValue > self.minMax[index].maxX)
              xValue = self.minMax[index].maxX;
            if (xValue < self.minMax[index].minX)
              xValue = self.minMax[index].minX;
            var x = self.graph.x(xValue);
  
            var yValue = self.fn(index, xValue);
            var y = self.graph.y(yValue);
            if (y < 0) y = 0;
  
            this.x ? (this.x.baseVal.value = x) : (this.cx.baseVal.value = x);
            this.y ? (this.y.baseVal.value = y) : (this.cy.baseVal.value = y);
            self.selected[index].x = xValue.toFixed(self.precision);
            self.selected[index].y = yValue.toFixed(self.precision);
  
            var text = "";
  
            if (
              [
                "independent",
                "single",
                "negative",
                "single_fixedsquare",
                "single_fixedcircle",
                "newone",
              ].indexOf(self.mode) !== -1
            ) {
              if (index == 0) {
                text =
                  "Tú (A: " +
                  xValue.toFixed(self.precision) +
                  ", B: " +
                  yValue.toFixed(self.precision) +
                  ")";
              } else {
                text =
                  "Pareja (A: " +
                  xValue.toFixed(self.precision) +
                  ", B: " +
                  yValue.toFixed(self.precision) +
                  ")";
              }
            } else if (self.mode === "single_given") {
              text =
                "Tu: " +
                xValue.toFixed(self.precision) +
                ", Pareja: " +
                yValue.toFixed(self.precision);
            } else if (self.mode === "positive") {
              text =
                "Tu = Pareja (A: " +
                xValue.toFixed(self.precision) +
                ", B: " +
                yValue.toFixed(self.precision) +
                ")";
            }
  
            if (self.tip && self.tip[index]) {
              self.tip[index]
                .attr("x", x + 15)
                .attr("y", y - 15)
                .text(text);
            }
  
            if (self.mode !== "probability") {
              var otherIndex = 1 - index;
              switch (self.mode) {
                /*case "negative":
                  var other = d3.select('[line-index="' + otherIndex + '"]');
                  var otherXValue = self.fnInverse(otherIndex, xValue);
                  if (otherXValue > self.minMax[otherIndex].maxX)
                    otherXValue = self.minMax[otherIndex].maxX;
                  if (otherXValue < self.minMax[otherIndex].minX)
                    otherXValue = self.minMax[otherIndex].minX;
                  var otherX = self.graph.x(otherXValue);
                  var otherYValue = xValue;
                  var otherY = self.graph.y(otherYValue);
                  if (otherY < 0) otherY = 0;
                  if (other.attr("cx")) {
                    other.attr("cx", otherX - self.circleRadius);
                    other.attr("cy", otherY - self.circleRadius);
                    me.attr("x", x);
                    me.attr("y", y);
                  } else {
                    other.attr("x", otherX - self.circleRadius);
                    other.attr("y", otherY - self.circleRadius);
                    me.attr("cx", x);
                    me.attr("cy", y);
                  }
                  self.selected[otherIndex].x = otherXValue.toFixed(
                    self.precision
                  );
                  self.selected[otherIndex].y = otherYValue.toFixed(
                    self.precision
                  );
                  var otherText = "";
                  if (otherIndex == 0) {
                    otherText =
                      "Tú (A: " +
                      otherXValue.toFixed(self.precision) +
                      ", B: " +
                      otherYValue.toFixed(self.precision) +
                      ")";
                  } else {
                    otherText =
                      "Pareja (A: " +
                      otherXValue.toFixed(self.precision) +
                      ", B: " +
                      otherYValue.toFixed(self.precision) +
                      ")";
                  }
                  if (self.tip && self.tip[otherIndex]) {
                    self.tip[otherIndex]
                      .attr("x", otherX + 15)
                      .attr("y", otherY - 15)
                      .text(otherText);
                  }
                  break;*/
                case "positive":
                  var other = d3.select('[line-index="' + otherIndex + '"]');
  
                  if (other.attr("cx")) {
                    other.attr("cx", x);
                    other.attr("cy", y);
                    me.attr("x", x - self.circleRadius);
                    me.attr("y", y - self.circleRadius);
                  } else {
                    other.attr("x", x - self.circleRadius);
                    other.attr("y", y - self.circleRadius);
                    me.attr("cx", x);
                    me.attr("cy", y);
                  }
  
                  self.selected[otherIndex].x = xValue.toFixed(self.precision);
                  self.selected[otherIndex].y = yValue.toFixed(self.precision);
  
                  var otherText = "";
  
                  if (otherIndex == 0) {
                    otherText =
                      "Tú = Pareja (A: " +
                      xValue.toFixed(self.precision) +
                      ", B: " +
                      yValue.toFixed(self.precision) +
                      ")";
                  }
  
                  if (self.tip && self.tip[otherIndex]) {
                    self.tip[otherIndex]
                      .attr("x", x + 15)
                      .attr("y", y - 15)
                      .text(otherText);
                  }
  
                  break;
                default:
                  me.attr("x", x - self.circleRadius);
                  me.attr("y", y - self.circleRadius);
                  break;
              }
            }
          });
  
          var generate = function () {
            if (self.mode === "probability") {
              self.prob.a = Math.random() * (100 - 0) + 0;
              ["a", "b"].forEach(function (s) {
                self.graph.svg
                  .append("circle")
                  .attr("r", self.radius[s])
                  .attr("line-index", s)
                  .attr("cx", function (d) {
                    return self.graph.x(self.equation[s].x);
                  })
                  .attr("cy", function (d) {
                    return self.graph.y(self.fn(index, self.equation[s].x));
                  });
                self.tip[s] = self.graph.svg
                  .append("text")
                  .attr("x", self.graph.x(self.equation[s].x) + 15)
                  .attr(
                    "y",
                    self.graph.y(self.fn(index, self.equation[s].x)) - 45
                  )
                  .text(null);
              });
              return;
            }
            if (index === 0) {
              var me = self.graph.svg
                .append("rect")
                .style("fill", self.mode === "single_given" ? "red" : "blue")
                .attr("width", self.squareLength)
                .attr("height", self.squareLength)
                .attr("line-index", index)
                .attr("x", function (d) {
                  return self.graph.x(randomX) - self.circleRadius;
                })
                .attr("y", function (d) {
                  return (
                    self.graph.y(self.fn(index, randomX)) - self.circleRadius
                  );
                });
  
              if (self.mode === "single_fixedsquare") return;
  
              me.call(drag);
            } else {
              var other = self.graph.svg
                .append("circle")
                .style("fill", "orange")
                .attr("r", self.circleRadius)
                .attr("line-index", index)
                .attr("cx", function (d) {
                  return self.graph.x(randomX);
                })
                .attr("cy", function (d) {
                  return self.graph.y(self.fn(index, randomX));
                });
  
              if (self.mode === "single_fixedcircle") return;
  
              other.call(drag);
            }
          };
          generate();
        }
      },
      start: function () {
        this.reset();
        this.sanity();
        this.plots();
        this.init();
        this.drawAxis();
        this.draw();
        this.showSelect();
      },
      update: function (newData) {
        d3.select("svg").remove();
        this.start();
      },
    },
    mounted: function () {
      this.start();
    },
  });
