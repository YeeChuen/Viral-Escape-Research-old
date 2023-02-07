def extract_protein_names(file_path):
    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith('>'):
                protein_description = line.strip()
                protein_name = protein_description.split('|')[0][1:]
                print(protein_name)

file_path = 'PoreDB_short.fas'
extract_protein_names(file_path)
