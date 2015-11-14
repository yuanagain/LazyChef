// Rushy Panchal
// lazychef.js

function LazyChef(data) {
	var timer = new Timer();
	var pointers = {
		active: 0,
		passive: 0,
		upcomingTimers: [null, null, null]
		}

	$("#control-play").click(function() {
		if (timer.isRunning()) {
			timer.stop();
			$(this).children("i").get(0).className = "fa fa-play";
			}
		else {
			timer.start();
			$(this).children("i").get(0).className = "fa fa-pause";
			}
		});

	timer.secondHook(0, updateActive);

	var passiveTemplate = document.getElementById("passive-task-nth");

	/* Queue up the passive tasks
	Although we are adding all of the tasks at once, they are only
	registered as tasks when the proper time occurs.
	If there are more than 3 concurrent passive tasks, then
	only the first 3 are shown (this is done via CSS). */
	for (var passiveIndex = 0; passiveIndex < data.passive.length; passiveIndex++) {
		var passiveTask = data.passive[passiveIndex];
		// this function hack is needed because we're iteratively creating functions
		(function(passiveTask, passiveIndex) {
			timer.secondHook(passiveTask.start_time, function() {
				// create DOM to display as clone of a mock template
				var taskDOM = passiveTemplate.cloneNode(true);
				taskDOM.id = "passive-task-" + passiveIndex;
				taskDOM.style.display = "block";
				taskDOM.querySelector(".name").innerHTML = passiveTask.name;
				taskDOM.querySelector(".timer").id = "passive-timer-" + passiveIndex;

				$("#background-tasks").append(taskDOM);

				passiveTimer = new TimerVisualizer("#passive-timer-" + passiveIndex, passiveTask.time_delta, passiveTask.end_time, passiveTask.name, timer, passive_color);
				passiveTimer.start();

				// function hack, similar to above
				(function(passiveTask, passiveIndex, passiveTimer) {
					timer.secondHook(passiveTask.end_time + 1, function() {
						// destroy the timer and remove the DOM element when finished
						passiveTimer.destroy();
						$("#passive-task-" + passiveIndex).remove();
						pointers.passive++;
						});
					})(passiveTask, passiveIndex, passiveTimer);
				});
			})(passiveTask, passiveIndex);
		}

	function updateActive() {
		// Update the current active task
		var task = data.active[pointers.active];
		$("#name").html(task.name);
		$("#description").html(task.description);
		taskTimer = new TimerVisualizer("#active-task-timer", task.time_delta, task.end_time, task.name, timer);
		taskTimer.start();
		updateUpcoming(pointers.active);
		timer.secondHook(task.end_time + 1, function() {
			// Remove the current task visualizer
			taskTimer.destroy();
			pointers.active++;
			if (pointers.active + 1 < data.active.length) updateActive();
			});
		}

	function updateUpcoming() {
		// Add three upcoming timers from the given index onwards
		for (var i = 1; i <= 3; i++) {
			// Clear current timers in upcoming display
			if (pointers.upcomingTimers[i] != null) {
				pointers.upcomingTimers[i].destroy();
				pointers.upcomingTimers[i] = null;
				$("#upcoming-name-" + i).html("");
				}

			// if pointer.active + 1 >= data.active.length, no more upcoming tasks
			if (pointers.active + i < data.active.length) {
				var upcomingTask = data.active[pointers.active + i];
				newTimer = new TimerVisualizer("#upcoming-timer-" + i, upcomingTask.time_delta, upcomingTask.end_time, upcomingTask.name, timer);
				pointers.upcomingTimers[i] = newTimer;

				$("#upcoming-name-" + i).html(upcomingTask.name);
				}
			}
		}
	}