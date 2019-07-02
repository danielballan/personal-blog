get_ipython().run_line_magic('matplotlib', 'qt5')
import matplotlib.pyplot as plt
fig, ax  = plt.subplots()
plt.xlim(0, 5.5)
plt.ylim(0, 5.5)
plt.xticks((1,2,3,4,5), ('1 person\n(you)', '5 people\n(team)', '100 people\n(group)', '10,000 people\n(division)', '1,000,000 people\n(world)'), rotation=-10)
plt.yticks((1,2,3,4,5), ('1 day', '1 week', '3 months', '1 year', '10 years'), rotation=30)
