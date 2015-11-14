// Rushy Panchal
// timer.js

function Timer() {
	// Create a timer counting seconds passed
	this.elapsed = 0;
	this.interval = null;
	this.hooks = [];
	}

Timer.prototype.second = function(hook) {
	// Add a callback for when a second passes
	this.hooks.push(hook);
	}

Timer.prototype.start = function() {
	// Start the timer
	if (this.interval == null) {
		var timer = this;
		this.interval = setInterval(function() {
			timer.elapsed++;
			for (var i = 0; i < timer.hooks.length; i++) {
				timer.hooks[i](timer.elapsed);
				}
			}, 1000);
		};
	}

Timer.prototype.stop = function() {
	// Stop the timer
	if (this.interval != null) {
		clearInterval(this.interval);
		this.interval = null;
		}
	}

Timer.prototype.reset = function() {
	// Reset the timer
	this.stop();
	this.elapsed = 0;
	}

function TimerVisualizer(element, totalSeconds, timer, config) {
	// Create a timer on the element with the amount of remaining time
	this.element = element;
	this.total = totalSeconds;
	this.timer = timer || new Timer();

	var visualizer = this;
	this.timer.second(function() {
		var timer = visualizer.timer;
		visualizer.circle.animate((visualizer.total - timer.elapsed) / visualizer.total,
			function() {
				visualizer.circle.setText(visualizer.total - timer.elapsed);
				});
			});
	
	this.circle = new ProgressBar.Circle(element, config || {
		color: "green",
		trailColor: "#ddd",
		trailWidth: 1,
		duration: 100,
		easing: 'linear',
		strokeWidth: 2,
		text: {
			className: "timer-text"
			}
		});
	this.circle.set(1);
	this.circle.setText(this.total);
	}

TimerVisualizer.prototype.start = function() {
	// Start the timer
	this.timer.start();
	}

TimerVisualizer.prototype.stop = function() {
	// Stop the timer
	this.timer.stop();
	}

TimerVisualizer.prototype.reset = function() {
	// Reset the timer
	this.timer.reset();
	this.circle.set(1);
	this.circle.setText(timer.total);
	}

TimerVisualizer.prototype.isRunning = function() {
	// Check if the Timer is running
	return this.timer.interval != null;
	}
