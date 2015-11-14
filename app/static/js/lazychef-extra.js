/* This block of code adds all of the tasks to the timer hooks
	from the beginning. When the start time of the task is reached,
	the hook is executed, by creating a timer visualizer.
	In addition, this hook adds another hook at the task's end time;
	this new hook removes the visualizer. */

for (var i = 0; i < input_data.active.length; i++) {
	var task = input_data.active[i];
	(function(task) {
		// the function hack is required for creating callbacks iteratively
		timer.secondHook(task.start_time, function() {
			$("#name").html(task.name);
			$("#description").html(task.description);
			// add each task as a callback to the timer
			taskTimer = new TimerVisualizer("#active-task-timer", task.time_delta, task.end_time, task.name, timer);
			updateUpcoming(pointers.active);
			timer.secondHook(task.end_time, function() {
				// remove the task visualizer
				taskTimer.destroy();

				pointers.active++;
				});
			});
		})(task);
	}