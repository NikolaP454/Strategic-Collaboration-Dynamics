import argparse

from envelop_game import perform_simulation

def get_args() -> argparse.ArgumentParser:
    '''
    Read the arguments from the command line and return them.
    
    Returns:
    --------
    
    argparser: argparse.ArgumentParser
        The argument parser.  
    '''
    
    # Create the argument parser
    argparser = argparse.ArgumentParser(description='Simulate the Envelope Game on a network')
    
    # Add the arguments
    argparser.add_argument(
        '--output_dir',
        type=str, 
        required=True,
        help='Output directory'
    )
    
    argparser.add_argument(
        '--graph_file',
        type=str, 
        required=True,
        help='Path to the graph file'
    )
    
    argparser.add_argument(
        '--type',
        type=int, 
        default=1,
        help='Type of simulation'
    )
    
    argparser.add_argument(
        '--step',
        type=int, 
        default=0,
        help='Number of steps'
    )
    
    # Parse the arguments
    return argparser

if __name__ == '__main__':
    # Get arguments
    args = get_args().parse_args()
    
    OUTPUT_DIR = args.output_dir
    GRAPH_FILE = args.graph_file
    TYPE = args.type
    STEP = args.step
    
    # Perform simulation
    if TYPE == 1:
        perform_simulation(OUTPUT_DIR, GRAPH_FILE, TYPE)
        
    elif TYPE == 2:
        perform_simulation(OUTPUT_DIR, GRAPH_FILE, TYPE, STEP)