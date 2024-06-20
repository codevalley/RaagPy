
import argparse

# Required tokens and normalization mapping for Indian classical music notations
tokens = ["s", "r", "g", "m", "p", "d", "n", "S", "R", "G", "M", "P", "D", "N", "s_", "r_", "g_", "m_", "p_", "d_", "n_"]
# mapping notes to their root value
normalization_map = {
    's_': 'S', 'r_': 'R', 'g_': 'G', 'm_': 'M', 'p_': 'P', 'd_': 'D', 'n_': 'N',
    's': 'S', 'r': 'R', 'g': 'G', 'm': 'M', 'p': 'P', 'd': 'D', 'n': 'N',
    'S': 'S', 'R': 'R', 'G': 'G', 'M': 'M', 'P': 'P', 'D': 'D', 'N': 'N',
}

scale_length = 7  # default length of the musical scale

def generate_scale_constants(scale):
    middle_octave = scale  # CAPS string, e.g., 'SGMDN'
    lower_octave = scale.lower()  # Convert to lower case for lower octave
    upper_octave = [char + '_' for char in lower_octave]  # Append '_' for upper octave
    tkns = list(lower_octave) + list(middle_octave)+upper_octave
    
    nmap = {}
    # Normalize upper octave tokens by removing underscores and converting to uppercase
    for char in upper_octave:
        nmap[char] = char[0].upper()
    # Normalize middle and lower octaves directly to their uppercase
    for char in middle_octave + lower_octave:
        nmap[char] = char.upper()

    scale_len = len(middle_octave)
    return tkns, nmap, scale_len

def next_token(token):
    if token in tokens:
        return tokens[(tokens.index(token) + 1) % len(tokens)]
    return token  # Return the special token unchanged

def previous_token(token):
    if token in tokens:
        return tokens[(tokens.index(token) - 1) % len(tokens)]
    return token  # Return the special token unchanged

def tokenize_pattern(pattern):
    result_tokens = []
    i = 0
    while i < len(pattern):
        if i + 1 < len(pattern) and (pattern[i:i+2] in tokens):
            result_tokens.append(pattern[i:i+2])
            i += 2
        elif pattern[i] in tokens:
            result_tokens.append(pattern[i])
            i += 1
        else:
            # Treat unrecognized characters or sequences as special tokens
            result_tokens.append(pattern[i])
            i += 1
    return result_tokens


def normalize_pattern(pattern):
    normalized = []
    tokens = tokenize_pattern(pattern)
    for token in tokens:
        if token in normalization_map:
            normalized.append(normalization_map[token])
        else:
            # Preserve the special tokens as they are
            normalized.append(token)
    return ''.join(normalized)


def comparePattern(pattern1, pattern2):
    return normalize_pattern(pattern1) == normalize_pattern(pattern2)

def mirror_seed(seed):
    mirrored_seed = []
    s_index = tokens.index('S')
    for token in tokenize_pattern(seed):
        if token in tokens: 
            current_index = tokens.index(token)
            delta_index = (current_index - s_index)
            new_index = (s_index + scale_length - delta_index) % len(tokens)
            mirrored_seed.append(tokens[new_index])
        else: 
            mirrored_seed.append(token)
    return ''.join(mirrored_seed)

def generate_patterns(seed, ascending=True):
    seed_to_use = mirror_seed(seed) if not ascending else seed
    original_pattern = tokenize_pattern(seed_to_use)
    current_pattern = original_pattern[:]
    patterns = []
    
    while True:
        patterns.append(current_pattern)  # Append the current pattern array of tokens
        next_pattern = [next_token(token) if ascending else previous_token(token) for token in current_pattern]
        if comparePattern(''.join(next_pattern), ''.join(original_pattern)):
            patterns.append(next_pattern)
            break
        current_pattern = next_pattern
    return patterns

def format_pattern(pattern):
    formatted_tokens = [(token + ' ') if len(token) == 1 and token != ' ' else token for token in pattern]
    return ''.join(formatted_tokens)  # Join 

def setup_arg_parser():
    parser = argparse.ArgumentParser(description="Generate Alankars for given Raag scale.")
    parser.add_argument("pattern", type=str, help="The seed pattern of the alankar, e.g., 'SGMDN'")
    parser.add_argument("-s", "--scale", type=str, default="SRGMPDNS", help="Optional scale input in CAPS for middle octave. Default is 'SRGMPDNS'")
    return parser
    
def main():
    parser = setup_arg_parser()
    args = parser.parse_args()
    global tokens
    global normalization_map
    global scale_length 
    # Generate scale constants based on input or default
    tokens, normalization_map, scale_length = generate_scale_constants(args.scale)
    # Generate patterns
    for pattern in generate_patterns(args.pattern, ascending=True):
        print(format_pattern(pattern))
    print("---------------------")
    for pattern in generate_patterns(args.pattern, ascending=False):
        print(format_pattern(pattern))

if __name__ == "__main__":
    main()

