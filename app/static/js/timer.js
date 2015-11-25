// Rushy Panchal
// timer.js

function Timer() {
	// Create a timer counting seconds passed
	this.elapsed = 0;
	this.interval = null;
	this.hooks = {};
	this.hooks[-1] = {};
	}

Timer.prototype.eachSecond = function(id, hook) {
	// Add a callback for each second with a given id
	this.hooks[-1][id] = hook;
	}

Timer.prototype.removeHook = function(id) {
	// Remove hook from a timer
	delete this.hooks[-1][id];
	}

Timer.prototype.secondHook = function(second, hook) {
	// Add a callback for when a specific second passes
	if (second < 0) return; // irrelevant hook
	if (this.hooks.hasOwnProperty(second)) this.hooks[second].push(hook);
	else this.hooks[second] = [hook];
	}

Timer.prototype.isRunning = function() {
	// Check if the timer is running
	return this.interval != null;
	}

Timer.prototype.start = function() {
	// Start the timer
	if (! this.isRunning()) {
		var timer = this;
		this.interval = setInterval(function() {
			if (timer.hooks.hasOwnProperty(timer.elapsed)) {
				// call each hook for each second
				for (var i = 0; i < timer.hooks[timer.elapsed].length; i++) {
					timer.hooks[timer.elapsed][i]();
					}
				delete timer.hooks[timer.elapsed]; // no way to use these hooks again
				}
			for (var key in timer.hooks[-1]) {
				timer.hooks[-1][key](timer.elapsed);
				}
			timer.elapsed++;
			}, 1000);
		}
	}

Timer.prototype.stop = function() {
	// Stop the timer
	if (this.isRunning()) {
		clearInterval(this.interval);
		this.interval = null;
		}
	}

Timer.prototype.reset = function() {
	// Reset the timer
	this.stop();
	this.elapsed = 0;
	}

function TimerVisualizer(element, delta, end, name, timer, color) {
	// Create a timer on the element with the amount of remaining time
	this.element = element;
	this.name = name;
	this.total = end;
	this.delta = delta;
	this.timer = timer;
	this.timer_id = Math.random(); // generate a random ID
	
	var options = {
		color: color || default_color,
		trailColor: "#ddd",
		trailWidth: 1,
		duration: 975,
		easing: 'linear',
		strokeWidth: 2,
		text: {
			className: "timer-text"
			}
		};

	this.circle = new ProgressBar.Circle(element, options);
	
	this.circle.set(1);
	this.setText(this.delta);
	}

TimerVisualizer.prototype.destroy = function() {
	// Destroy the timer visualizer
	this.circle.destroy();
	this.stop();
	}

TimerVisualizer.prototype.start = function() {
	// Start the timer
	var visualizer = this;
	this.timer.eachSecond(this.timer_id, function(currentTime) {
		var timer = visualizer.timer;
		visualizer.circle.animate((visualizer.total - currentTime) / visualizer.delta,
			function() {
				visualizer.setText(visualizer.total - currentTime);
				});
		});
	}

TimerVisualizer.prototype.stop = function() {
	// Stop the timer
	this.timer.removeHook(this.timer_id);
	}

TimerVisualizer.prototype.reset = function() {
	// Reset the timer
	this.setTotal(this.timer.total);
	}

TimerVisualizer.prototype.setTotal = function(name, value) {
	// Set the total value and reset the timer
	this.name = name;
	this.circle.set(1);
	this.total = value;
	this.setText(value);
	}

TimerVisualizer.prototype.setText = function(value) {
	// Set the text for the timer visualizer
	var text, momentTime = moment().set({hours: 0, minutes: 0, seconds: value});
	if (value > 3600) text = momentTime.format("HH:mm:ss");
	else text = momentTime.format("mm:ss");

	this.circle.setText(text);
	}

TimerVisualizer.prototype.isRunning = function() {
	// Check if the Timer is running
	return this.timer.isRunning();
	}
