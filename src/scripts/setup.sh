# cleanup() {
# 	    # kill all processes whose parent is this process
# 	        pkill -P $$
# 		pkill flask
# 	}

# for sig in INT QUIT HUP TERM; do
# 	  trap "
# 	      cleanup
# 	          trap - $sig EXIT
# 		      kill -s $sig "'"$$"' "$sig"
# 	      done
# 	      trap cleanup EXIT
# cwd=$(pwd)
# echo ${cwd}
# run frontend
./frontend.sh
# run users
./user.sh
# run auctions
./auctions.sh
# run items
./items.sh


# pkill flask to kill all
