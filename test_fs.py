from bin.jf_filereader import JFFileReader

FR = JFFileReader('test.jf')

print(FR.LPF__EPISODE_LENGTH,FR.LPF__NAME)

FR.write()