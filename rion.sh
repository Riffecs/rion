pip uninstall rion -y
pip install git+https://github.com/Riffecs/rion.git#egg=rion
rm -rf rion
rion installer
rion server 139.162.141.181 2121
rion login user aghast-unhealthy-sloppy-elastic-referable
clear
echo "Load Rion"
echo " "
cat ~/rion/rion.conf
