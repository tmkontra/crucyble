poetry build
tar -xzf dist/*.tar.gz
DIST_FOLDER=$(ls | grep crucyble)
echo "Building in: ${DIST_FOLDER}"
DESC=$(echo "Description: " | cat - README.md)
DESC_TYPE=$(echo "Description-Content-Type: text/markdown")
echo "$DESC_TYPE" >> $DIST_FOLDER/PKG-INFO
echo "$DESC" >> $DIST_FOLDER/PKG-INFO
LDCT="    'long_description_content_type': 'text/markdown',"
sed -i "/'packages': packages/a${LDCT}" $DIST_FOLDER/setup.py
SDIST=${DIST_FOLDER}.tar.gz
tar -czf $SDIST $DIST_FOLDER
twine check $SDIST
