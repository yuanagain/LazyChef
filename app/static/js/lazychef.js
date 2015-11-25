// Rushy Panchal
// lazychef.js

function LazyChef(data) {
	// LazyChef main function
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

	$("#start-timers").click(function() {
		if (! timer.isRunning()) {
			timer.start();
			$(this).remove();
			$("#control-play").removeClass("hidden").children("i").get(0).className = "fa fa-pause";
			}
		});

	// var totalTimer = new TimerVisualizer("#total-timer", data.end_time, data.end_time, "Overall", timer, passive_color);
	// totalTimer.start();

	fixIdleGaps(data.active);
	timer.secondHook(0, updateActive);
	queuePassiveTasks(data);

	console.log(data);

	function updateActive() {
		// Update the current active task
		var task = data.active[pointers.active];

		// display the new timer and its given data
		$("#name").html(task.name);
		$("#description").html(task.description);
		taskTimer = new TimerVisualizer("#active-task-timer", task.time_delta, task.end_time, task.name, timer);
		taskTimer.start();

		// update the upcoming timers
		updateUpcoming(pointers.active);

		timer.secondHook(task.end_time + 1, function() {
			// Remove the current task visualizer
			taskTimer.destroy();
			pointers.active++;
			if (pointers.active < data.active.length) updateActive();
			else { // no more items left
				$("#name").html("");
				$("#description").html("");
				$("#done-notification").css("display", "block");
				$("#active-task-timer").remove();
				$("#control-play i").remove();
				}
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
				// display the upcoming timer if it exists
				var upcomingTask = data.active[pointers.active + i];
				newTimer = new TimerVisualizer("#upcoming-timer-" + i, upcomingTask.time_delta, upcomingTask.end_time, upcomingTask.name, timer);
				pointers.upcomingTimers[i] = newTimer;

				$("#upcoming-name-" + i).html(upcomingTask.name);
				}
			else break;
			}
		}

	function queuePassiveTasks(data) {
		// Queue the passive tasks
			var passiveTemplate = document.getElementById("passive-task-nth");

			/* Queue up the passive tasks
			Although we are adding all of the tasks at once, they are only
			registered as tasks when the proper time occurs.
			If there are more than 3 concurrent passive tasks, then
			only the first 3 are shown (this is done via CSS). */
			for (var passiveIndex = 0; passiveIndex < data.passive.length; passiveIndex++) {
				var passiveTask = data.passive[passiveIndex];
				// this function hack is needed because we're iteratively creating functions
				if (passiveTask.time_delta == 0) continue;
				(function(passiveTask, passiveIndex) {
					timer.secondHook(passiveTask.start_time, function() {
						// create DOM to display as clone of a mock template
						var taskDOM = passiveTemplate.cloneNode(true);
						taskDOM.id = "passive-task-" + passiveIndex;
						taskDOM.style.display = "block";
						taskDOM.querySelector(".name").innerHTML = passiveTask.name;
						taskDOM.querySelector(".timer").id = "passive-timer-" + passiveIndex;

						$("#background-tasks").append(taskDOM);

						// create Timer to display the timer countdown
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
		}

	function fixIdleGaps(array) {
		// Fix gaps of idle spaces in an array
		var index = 0;
		// can't just use a for loop because the array is actively being resized
		while (index + 1 < array.length) {
			var current = array[index],
				next = array[index + 1],
				time_diff = next.start_time - current.end_time;
			if (time_diff > 0) {
				// Fill empty spaces between active nodes with "idle" nodes
				var mockTask = {name: "Idle", "description": "", "start_time": current.end_time, "end_time": next.start_time, "time_delta": time_diff};
				// Insert into the array at a given position
				array.splice(index + 1, 0, mockTask);
				index++; // need to skip the newly inserted idle node
				}
			index++;
			}
		}
	}