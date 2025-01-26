import argparse

def get_arguments():
    '''
    Read the arguments from the command line and return them.
    
    Returns:
    --------
    
    args: argparse.Namespace
        The arguments read from the command line.    
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
    
    # Parse the arguments
    return argparser.parse_args()