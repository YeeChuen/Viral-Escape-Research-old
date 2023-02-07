from Bio.Seq import Seq
from Bio.Align import PairwiseAligner

#learn how to use Bio.Align.PairwiseAligner

# Define two protein sequences
seq1 = Seq("LQTQFYLEFGLM", "generic_protein")
seq2 = Seq("LQTQFYQEFGLM", "generic_protein")

# Define the PairwiseAligner object
pairwise_aligner = PairwiseAligner()

# Set the sequences to be aligned
pairwise_aligner.set_seqs(seq1, seq2)

# Perform the alignment
alignment = pairwise_aligner.align[0]

# Get the score of the alignment
score = alignment.score

print("Pairwise score:", score)
