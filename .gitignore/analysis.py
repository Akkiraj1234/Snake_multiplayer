import matplotlib.pyplot as plt
import pandas as pd

# Given data: RAM usage (in bytes) and time (in milliseconds)
data = [
    (25800704, 1717315130720145700), (28495872, 1717315130836153800), (28516352, 1717315130995146600),
    (28520448, 1717315131195146400), (28692480, 1717315131930930400), (28696576, 1717315134883398000),
    (28700672, 1717315136201927000), (28696576, 1717315138024296100), (28700672, 1717315147611016900),
    (28696576, 1717315150812101100), (28729344, 1717315160731770700), (28733440, 1717315160847999400),
    (28737536, 1717315165305455100), (28749824, 1717315165365482300), (28794880, 1717315165490893000),
    (28803072, 1717315165736078600), (28856320, 1717315165858968500), (28860416, 1717315173317525400),
    (28864512, 1717315173814097900), (28868608, 1717315179528553900), (28876800, 1717315179902756100),
    (28880896, 1717315184122632600), (28884992, 1717315185861127600), (28889088, 1717315186484262600),
    (28827648, 1717315190590777900), (28831744, 1717315192208628500), (28844032, 1717315193945928200),
    (28852224, 1717315194816352400), (28856320, 1717315198675913800), (28864512, 1717315204153657800),
    (28868608, 1717315204902447000), (28893184, 1717315205645910900), (28901376, 1717315208656472700),
    (28909568, 1717315208781177700), (28913664, 1717315210890911700), (28917760, 1717315213249966800),
    (28921856, 1717315217225026000), (28925952, 1717315219707866800), (28930048, 1717315223564496200),
    (28934144, 1717315223687711200), (28938240, 1717315229150814600), (28942336, 1717315231136864500),
    (28946432, 1717315233524380000), (28950528, 1717315242225501200), (28954624, 1717315242601144800),
    (28958720, 1717315244960453300), (28962816, 1717315248688977300), (28966912, 1717315252786944700),
    (28971008, 1717315254905208600), (28975104, 1717315255153092500), (28983296, 1717315255277723200),
    (28987392, 1717315261256589100), (28999680, 1717315261506355400), (29007872, 1717315261630482500),
    (29011968, 1717315262626649600), (28983296, 1717315264486770000), (28987392, 1717315267590660100),
    (28995584, 1717315269580533500), (29003776, 1717315269704380400), (29007872, 1717315269950790900),
    (29016064, 1717315270075335600), (29020160, 1717315272192984600), (29024256, 1717315272448540000),
    (29024256, 1717315275342059600), (29036544, 1717315296398395300), (29036544, 1717315297894362200),
    (29044736, 1717315298140671600), (29077504, 1717315298389023800), (29081600, 1717315298516078600),
    (29093888, 1717315299011256200), (29097984, 1717315299136183400)
]

# Convert the data into a pandas DataFrame
df = pd.DataFrame(data, columns=['Bytes', 'Time_ms'])

# Convert time from milliseconds to seconds and normalize
df['Time_s'] = (df['Time_ms'] - df['Time_ms'].iloc[0]) / 1e9  # Convert to seconds and normalize

# Plot the data
plt.figure(figsize=(12, 6))
plt.plot(df['Time_s'], df['Bytes'], marker='o', linestyle='-', color='b')
plt.title('RAM Usage Over Time')
plt.xlabel('Time (seconds)')
plt.ylabel('RAM Usage (bytes)')
plt.grid(True)
plt.show()

# Identify significant changes in RAM usage
df['RAM_Change'] = df['Bytes'].diff().fillna(0)
significant_changes = df[df['RAM_Change'].abs() > df['RAM_Change'].std()]

# Generate report of significant changes
significant_changes_report = significant_changes[['Time_s', 'Bytes', 'RAM_Change']]

significant_changes_report


# import psutil
# import os 
# import time
# old = 0
# list1 = []

# def get_memory_usage():
#     global old
#     process = psutil.Process(os.getpid())
#     mem_info = process.memory_info()
#     ll=mem_info.rss
#     if not (old == ll):
#         list1.append((ll,time.time_ns()))
#         old = ll
#     os.system('cls')
#     print(ll, f"-  {ll / (1024 * 1024):.2f} MB")
#     print(list1)