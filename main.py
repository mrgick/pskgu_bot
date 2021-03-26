
import rasp.parser
from generate_route import generate_route, go_to_path, get_root
from tests.test_parser import test_parser
from tests.test_logger import test_logger

def main():
    test_parser()
    #test_logger()
    generate_route()
    print(get_root().children_dict["fulltime"].children_dict) 
main()
