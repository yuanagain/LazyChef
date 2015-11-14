function LazyChef(data) {
	var timer = new Timer();
	var pointers = {
		active: 0,
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

	function updatePassive() {
		// Update the listing of passive tasks
		
		}
	}