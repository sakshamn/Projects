
usage() {
    # -s for spider name, -p for project name, -d for domain name #
    # -r for run scrapy #
    echo "Usage:\n $0 [-p <project_name>] [-d <domain_name>] [-s <spider_name>] [-r <Y|N>] 1>&2; exit 1;"
}

# getopts: usage: getopts optstring name [arg] #
# using "p:" means we are to pass -p <argname>. #
# The ":" is used to specify that an argument is required after -p. #
# If ":" is not used then an argument is not required after -p. #
while getopts "p:r:d:s:" opt
do
    case $opt in
        p)
            project_name=$OPTARG
	    ;;
        d)
	    domain_name=$OPTARG
	    ;;
        s)
	    spider_name=$OPTARG
	    ;;
        r)
            (($opt == "Y" || $opt == "N")) || usage
            scrapy=$OPTARG
	        ;;
        h|*)
            usage
            exit
            ;;
    esac
done
echo $project_name

if [[ $scrapy == "Y" ]]
then
    echo "\nReceived Y. Starting with scrapy project...\n"

    scrapy startproject $project_name

    # This is where we will be saving our spiders (crawlers). #
    cd $project_name/$project_name/spiders

    # Run the following command to generate a spider with some initial code. #
    scrapy genspider $spider_name $domain_name
else
    echo "\nReceived $scrapy. Taking it as a No and not running scrapy...\n"
fi

echo "Shall we run the spider $spider_name now? Y/N:\t"
read input 
if [[ $input == "Y" ]]
then
    scrapy crawl $spider_name
fi

