poetry build -f sdist
tar -xzf dist/*.tar.gz
DIST_FOLDER=$(ls | grep crucyble)
echo "Building in: ${DIST_FOLDER}"
DESC=$(echo "Description: " | cat - README.md)
DESC_TYPE=$(echo "Description-Content-Type: text/markdown")
PKG_INFO="$DIST_FOLDER/PKG-INFO"
echo "$DESC_TYPE" >> $PKG_INFO
echo "$DESC" >> $PKG_INFO
# add classifiers to PKG-INFO
while read -r line;
    do sed -i "/Requires-Python:/aClassifier: $line" $PKG_INFO;
done < etc/classifiers.txt
cat $PKG_INFO
# set long description content type in setup.py
LDCT="    'long_description_content_type': 'text/markdown',"
sed -i "/'packages': packages/a${LDCT}" $DIST_FOLDER/setup.py
SDIST=${DIST_FOLDER}.tar.gz
tar -czf $SDIST $DIST_FOLDER
twine check $SDIST
