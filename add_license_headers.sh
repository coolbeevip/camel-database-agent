#!/bin/bash

find camel_database_agent -type f -name "*.py" | while read -r file
do
  if ! grep -q Copyright "$file"
  then
    # cat LICENSE_HEADER.tpl "$file" >"$file.new" && mv "$file.new" "$file"
    { cat LICENSE_HEADER.tpl; echo; cat "$file"; } >"$file.new" && mv "$file.new" "$file"
  fi
done