ClarTable
=========
About
-----
*ClarTable* is a python script for generating html table containing data about corpora from .csv file.


## Usage
```bash
usage: run.py [-h] [-i PATH] [-r PATH] [-o PATH]

Create html table from given data and rules

optional arguments:
  -h, --help  show this help message and exit
  -i PATH     path to input csv file
  -r PATH     path to json file with rules
  -o PATH     path to file where output html table will be written
```

## Rules format
Rules are composed of nested json notation of tags and field. 
Given rule:
```
{"tags": [
	{"tag": "<table>", "tags": [
		{"tag": "<thead>", "tags": [
			{"tag": "<th>", "text": "Some header"}	
		]},
		{"tag": "<tbody>", "tags": [
			{"tag": "<p>", "text": "Some text here", "fields": [
				{"text": "<strong>Field data</strong> will be inserted here: %s", "columns": ['column_name_in_csv_file']}
			]}
		]}
	]}
]}
```

Generated html code will be:
```
<table>
	<thead>
		<th>Some header
		</th>
	</thead>
	<tbody>
		<p>Some text here
			<strong>Field data</strong> will be inserted here: data_from_FIRST_row_in_csv_here
		</p>
	</tbody>
        <tbody>
                <p>Some text here
                        <strong>Field data</strong> will be inserted here: data_from_SECOND_row_in_csv_here
                </p>
        </tbody>
	[...]
        <tbody>
                <p>Some text here
                        <strong>Field data</strong> will be inserted here: data_from_LAST_row_in_csv_here
                </p>
        </tbody>
</table>

```

\<tbody\> tag encloses tags and fields for row creation, only tags nested within \<tbody\> ... \</tbody\> can contain "fields": []

	
