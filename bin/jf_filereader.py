def get_var(text: str) -> list[str, str]:
    """Extracts a variable name and its value from a string.

    This function attempts to split the input string `text` based on common
    assignment operators (' = ', ' =', or '= '). It iterates through these
    delimiters and returns the split parts as a list of two strings (variable
    name and value) if a split results in exactly two parts.

    Args:
        
        text: The input string containing a variable assignment (e.g., "my_var = some_value").

    Returns:
        
        A list containing two strings: [variable_name, value]

    Raises:
        
        SyntaxError: If the input string cannot be successfully split into
                     a variable and a value using the defined delimiters.
    """
    for i in (text.split(' = '), text.split(' ='), text.split('= ')):
        l = len(i)
        if l == 2:
            return i
    else:
        raise SyntaxError('JFFileError')

def get_var_w_type(text: str) -> list[str, str]:

    for i in (text.split(' = '), text.split(' ='), text.split('= ')):
        l = len(i)
        if l == 2:
            v,t = i[0].split('$')
            return v,t,i[1]
    else:
        raise SyntaxError('JFFileError')

def get_type(text: str) -> type:
    match text:
        case 'int':
            return int
        case 'float':
            return float
        case _:
            return str

class JFFileReader:
    def __init__(self,filepath: str):
        self.filepath = filepath
        self.load()
    def __getattr__(self, name):
        """
        SECTIONTITLE__VAR
        """
        sec, var = name.split('__')
        return self.pool[f'<{sec}>::{var}']
    def load(self):
        with open(self.filepath) as file_read:
            data = file_read.read()
        pool = {}
        current_segment = ''
        for line in data.splitlines():
            if not line: continue
            if line.startswith('<') and line.endswith('>'):
                # This is a segment
                if ' ' in line:
                    raise SyntaxError('No spaces allowed in Sections')
                current_segment = line
            elif not line.startswith('%') and not line.startswith('?'):
                # this is a variable
                if '$' in line:
                    # this means the variable has a special type
                    
                    var,typ, val = get_var_w_type(line)
                    t = get_type(typ)
                    pool[f'{current_segment}::{var}'] = t(val)
                    
                else:
                    # No type defined so it will be a string
                    
                    var, val = get_var(line)
                    pool[f'{current_segment}::{var}'] = val
            elif line.startswith('%'):
                # A List object will be created
                pool[f'{current_segment}::{line[1:]}'] = []
            elif line.startswith('?'):
                # add objects to list
                key, *rest = line[1:].split('::')
                for r in rest:
                    if '$' in r:
                        # hasattr
                        val,typ = r.split('$')
                        t = get_type(typ)
                        pool[f'{current_segment}::{key}'].append(t(val))
                    else:
                        pass
                        pool[f'{current_segment}::{key}'].append(r)
        self.pool = pool