```html
	<div>
				<label
					for="course_level"
					class="block text-sm"></label>
				<select
					name="course_level"
					value="{{course.course_level}}"
					id="course_level"
					class="m focus:border-indigo-500 sm:text-sm">
					{%for value, display in LEVEL_CHOICES%}
					<option value="{{value}}" {% if course.course_level == value %}selected{%endif%}>{{display}}</option>
					{%endfor%}
				</select>
			</div>
```

is equivalent to

```html
<option value="beginner">Beginner</option>
<option value="intermediate" selected>Intermediate</option>
<option value="advanced">Advanced</option>
```
