git pull 
black *
git add *
UUID=$(cat /proc/sys/kernel/random/uuid)
git commit -m $UUID
git push
clear
echo "Bitte warte"
sleep 7
clear
sh ~/rion.sh
reset
