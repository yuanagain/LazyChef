// Rushy Panchal
// timer.js

function Timer(element, totalSeconds, config) {
	// create a timer on the element with the amount of remaining time
	this.element = element;
	this.total = totalSeconds;
	this.elapsed = 0;
	this.interval = null;
	this.circle = new ProgressBar.Circle(element, config || {
		color: "#FCB03C",
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

Timer.prototype.start = function() {
	// Start the timer
	if (this.interval == null) {
		var timer = this;
		this.interval = setInterval(function() {
			timer.elapsed++;
			timer.circle.animate((timer.total - timer.elapsed) / timer.total, function() {
				timer.circle.setText(timer.total - timer.elapsed);
				});
			}, 1000);
		}
	return this.interval;
	}

Timer.prototype.stop = function() {
	// Stop the timer
	if (this.interval == null) return false;
	else {
		clearInterval(this.interval);
		this.interval  = null;
		return true;
		}
	}

Timer.prototype.reset = function() {
	// Reset the timer
	this.stop();
	this.elapsed = 0;
	this.circle.set(1);
	this.circle.setText(timer.total);
	}

Timer.prototype.isRunning = function() {
	// Check if the Timer is running
	return this.interval != null;
	}
