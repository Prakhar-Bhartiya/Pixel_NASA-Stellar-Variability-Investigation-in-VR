import lightkurve as lk
import matplotlib.pyplot as plt
search_results = lk.search_lightcurve('Pi Mensae', mission='TESS', author='SPOC')
# The index here refers to the first column of the search_results table above.
lc = search_results[0].download()


#plt.plot(x,y) x = flux and y = time
# plt.plot(lc.time.value, lc.flux.value)
plt.scatter(lc.time.value, lc.flux.value)
plt.xlabel("Time")
plt.ylabel("Flux Value")
# plt.show()
plt.savefig('plot.jpg')
# plt.show()
