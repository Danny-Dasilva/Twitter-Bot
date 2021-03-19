SOMETHING="storage/emulated/0/Music"
#echo $DIST 
adb shell 'cd storage/emulated/0/Music && for f in *\ *; do mv "$f" "${f// /_}"; done'
python3 adb-sync.py --reverse "${SOMETHING}/University_of_North_Texas_One_O'Clock_Lab_Band_Radio" ~/Music
adb shell "cd $SOMETHING && rm -rf University_Of*"
