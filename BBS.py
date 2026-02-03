def BBS(p,q,Xo,length_of_sequence):
    sequence = []
    Xn = Xo
    M = p*q
    for _ in range(length_of_sequence):
        Xn = (Xn**2)%M
        sequence.append(Xn)
    return sequence


def generate_p_and_q(min_length,max_length):
    


if __name__ == "__main__":