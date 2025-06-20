from bin.jf_filereader import JFFile

FR = JFFile('test.jf')

print(FR.LPF__EPISODE_LENGTH,FR.LPF__NAME)

FR.set('<LPF>::EPISODE_LENGTH',1200)
FR.write()
