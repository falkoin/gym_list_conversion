# imports
import pandas as pd
import os
from more_itertools import strip

# PDF processing

df_data = pd.read_csv('data.csv')
for idx, row in df_data.iterrows():

    event_phase = row['Event Phase'] # qual, semi, final
    association = row['Association'] # europe, world

    first_page = str(row['First'])
    last_page = str(row['Last'])
    output_name = row['Output']
    input_name = '"' + row['Input'] + '"'

    os.system('gs -sDEVICE=txtwrite -dFirstPage=' + first_page + ' -dLastPage=' + last_page + ' -o ' + output_name + '.txt ' + input_name)

    # Detect lines with information
    if association == 'world':
        if event_phase == 'qual':
            file1 = open(output_name + '.txt', 'r')
            Lines = file1.readlines()
            
            count = 0
            entry_counts = []

            for line in Lines:
                if "1st" in line and not "DNS" in line:
                    entry_counts.append(count)
                elif "2nd" in line and not "DNS" in line:
                    entry_counts.append(count)
                count += 1
        else:
            file1 = open(output_name + '.txt', 'r')
            Lines = file1.readlines()
            
            count = 0
            rank_count = 1
            entry_counts = []
            for line in Lines:
                stripped_line = line.strip().split()
                if len(stripped_line) > 4 and stripped_line[0] == str(rank_count):
                    entry_counts.append(count)
                    rank_count += 1
                count += 1

    elif association == 'europe':
        file1 = open(output_name + '.txt', 'r')
        Lines = file1.readlines()
        
        count = 0
        rank_count = 1
        entry_counts = []
        for line in Lines:
            stripped_line = line.strip().split()
            if stripped_line[0] == str(rank_count) and len(stripped_line) > 8:
                entry_counts.append(count)
                rank_count += 1
            count += 1
    else:
        print("Wrong association")


    # Processing information to dataframe
    df = pd.DataFrame()
    if association == 'world':
        if event_phase == 'qual':
            header = ("Rank", "Routine", "Name", "D", "E", "T", "H", "Pen.", "Total", "End", "Country", "Qualified")
            df = pd.DataFrame(columns=header)

            df_pos = 0
            for entry in entry_counts:
                
                if df_pos%2 == 0:
                    corrector = 1
                else:
                    corrector = -1

                current_entry = Lines[entry].strip().split()
                corrected_entry = Lines[entry+corrector].strip().split()

                rank = int(corrected_entry[0])
                routine = current_entry[0]
                d = float(current_entry[1])
                e = float(current_entry[2])
                t = float(current_entry[3])
                h = float(current_entry[4])

                if len(current_entry) is 7:
                    penalty = 0.0
                    total = current_entry[5]
                else:
                    penalty = current_entry[5]
                    total = current_entry[6]


                if len(corrected_entry) is 6:

                    if len(corrected_entry[-1]) > 3:
                        name = corrected_entry[1] + " " + corrected_entry[2] + " " + corrected_entry[3]
                        country = corrected_entry[4]
                        end_added = corrected_entry[5]
                    else:
                        name = corrected_entry[1] + " " + corrected_entry[2]
                        country = corrected_entry[3]
                        end_added = corrected_entry[4]

                    if corrected_entry[-1].isupper():
                        qualified = corrected_entry[-1]
                    else:
                        qualified = ' '

                elif len(corrected_entry) is 7:
                    name = corrected_entry[1] + " " + corrected_entry[2] + " " + corrected_entry[3]
                    country = corrected_entry[4]
                    end_added = corrected_entry[5]

                    if corrected_entry[-1].isupper():
                        qualified = corrected_entry[-1]
                    else:
                        qualified = ' '

                elif len(corrected_entry) is 8:
                    name = corrected_entry[1] + " " + corrected_entry[2] + " " + corrected_entry[3] + " " + corrected_entry[4]
                    country = corrected_entry[5]
                    end_added = corrected_entry[6]

                    if corrected_entry[-1].isupper():
                        qualified = corrected_entry[-1]
                    else:
                        qualified = ' '
                else:
                    qualified = ""
                    name = corrected_entry[1] + " " + corrected_entry[2]
                    country = corrected_entry[3]
                    end_added = corrected_entry[4]

                    if corrected_entry[-1].isupper():
                        qualified = corrected_entry[-1]
                    else:
                        qualified = ' '

                df.loc[df_pos] = (rank,
                                  routine,
                                  name,
                                  d, 
                                  e,
                                  t,
                                  h,
                                  float(penalty),
                                  float(total),
                                  end_added,
                                  country,
                                  qualified
                                 )  
                
                if df_pos == len(entry_counts)-3:
                    break
                df_pos += 1
            df.to_csv(output_name + ".csv", index=False)
        elif event_phase == "semi":
            header = ("Rank", "Name", "D", "E", "T", "H", "Pen.", "Total", "Country", "Qualified")
            df = pd.DataFrame(columns=header)

            df_pos = 0
            for entry in entry_counts:

                current_entry = Lines[entry].strip().split()
                next_entry = Lines[entry+1].strip().split()

                if current_entry[3].isupper() == False and current_entry[4].isupper() == True:
                    rank = int(current_entry[0])
                    name = current_entry[1] + ' ' + current_entry[2] + ' ' + current_entry[3]
                    country = current_entry[4]
                    total = current_entry[5]
                    d = next_entry[0]
                    e = next_entry[1]
                    t = next_entry[2]
                    h = next_entry[3]
                    if len(next_entry) == 4:
                        pen = 0.00
                    else:
                        pen = next_entry[4]
                    if current_entry[-1].isupper():
                        qualified = current_entry[-1]
                    else:
                        qualified = ' '
                elif current_entry[4].isupper() == False and len(current_entry) > 6:
                    rank = int(current_entry[0])
                    name = current_entry[1] + ' ' + current_entry[2] + ' ' + current_entry[3] + ' ' + current_entry[4]
                    # print(current_entry)
                    country = current_entry[5]
                    total = current_entry[6]
                    d = next_entry[0]
                    e = next_entry[1]
                    t = next_entry[2]
                    h = next_entry[3]
                    if len(next_entry) == 4:
                        pen = 0.00
                    else:
                        pen = next_entry[4]
                    if current_entry[-1].isupper():
                        qualified = current_entry[-1]
                    else:
                        qualified = ' '
                else:
                    rank = int(current_entry[0])
                    name = current_entry[1] + ' ' + current_entry[2]
                    country = current_entry[3]
                    total = current_entry[4]
                    d = next_entry[0]
                    e = next_entry[1]
                    t = next_entry[2]
                    h = next_entry[3]
                    if len(next_entry) == 4:
                        pen = 0.00
                    else:
                        pen = next_entry[4]
                    if current_entry[-1].isupper():
                        qualified = current_entry[-1]
                    else:
                        qualified = ' '


                df.loc[df_pos] = (rank,
                                  name,
                                  d, 
                                  e,
                                  t,
                                  h,
                                  pen,
                                  total,
                                  country,
                                  qualified
                                )  
                
                df_pos += 1
                # header = ("Rank", "Routine", "Name", "D", "E", "T", "H", "Pen.", "Total", "End", "Country", "Qualified")
            df.to_csv(output_name + ".csv", index=False)
        elif event_phase == "final":
            header = ("Rank", "Name", "D", "E", "T", "H", "Pen.", "Total", "Country")
            df = pd.DataFrame(columns=header)

            df_pos = 0
            for entry in entry_counts:

                current_entry = Lines[entry].strip().split()
                next_entry = Lines[entry+1].strip().split()

                if current_entry[3].isupper() == False:
                    rank = int(current_entry[0])
                    name = current_entry[1] + ' ' + current_entry[2] + ' ' + current_entry[3]
                    country = current_entry[4]
                    total = current_entry[5]
                    d = next_entry[0]
                    e = next_entry[1]
                    t = next_entry[2]
                    h = next_entry[3]
                    if len(next_entry) == 4:
                        pen = 0.00
                    else:
                        pen = next_entry[4]
                elif current_entry[4].isupper() == False and len(current_entry) > 5:
                    rank = int(current_entry[0])
                    name = current_entry[1] + ' ' + current_entry[2] + ' ' + current_entry[3] + ' ' + current_entry[4]
                    country = current_entry[5]
                    total = current_entry[6]
                    d = next_entry[0]
                    e = next_entry[1]
                    t = next_entry[2]
                    h = next_entry[3]
                    if len(next_entry) == 4:
                        pen = 0.00
                    else:
                        pen = next_entry[4]
                else:
                    rank = int(current_entry[0])
                    name = current_entry[1] + ' ' + current_entry[2]
                    country = current_entry[3]
                    total = current_entry[4]
                    d = next_entry[0]
                    e = next_entry[1]
                    t = next_entry[2]
                    h = next_entry[3]
                    if len(next_entry) == 4:
                        pen = 0.00
                    else:
                        pen = next_entry[4]


                df.loc[df_pos] = (rank,
                                  name,
                                  d, 
                                  e,
                                  t,
                                  h,
                                  pen,
                                  total,
                                  country
                                )  
                
                df_pos += 1
                # header = ("Rank", "Routine", "Name", "D", "E", "T", "H", "Pen.", "Total", "End", "Country", "Qualified")
            df.to_csv(output_name + ".csv", index=False)
        else:
            print('Error in Association: world event phase')

    elif association == 'europe':
        if event_phase == 'qual':
            header = ("Rank", "Routine", "Name", "D", "E", "T", "H", "Pen.", "Total", "End", "Country", "Qualified")
            df = pd.DataFrame(columns=header)

            df_pos = 0
            for entry in entry_counts:

                corrector = 1
                current_entry = Lines[entry].strip().split()
                corrected_entry = Lines[entry+corrector].strip().split()
                
                if len(current_entry) < 13:
                    rank = int(current_entry[0])
                    routine = current_entry[4]
                    name = current_entry[1] + ' ' + current_entry[2]
                    d = 0.00
                    e = 0.00
                    t = 0.00
                    h = 0.00
                    pen = 0.00
                    total = 0.00
                    end_score = current_entry[11]
                    country = current_entry[3]
                    if current_entry[-1].isupper():
                        qualified = current_entry[-1]
                    else:
                        qualified = ' '
                elif current_entry[3].isupper() == False:
                    rank = int(current_entry[0])
                    routine = current_entry[5]
                    name = current_entry[1] + ' ' + current_entry[2] + ' ' + current_entry[3]
                    d = current_entry[8]
                    e = current_entry[6]
                    t = current_entry[7]
                    h = current_entry[9]
                    pen = current_entry[12]
                    total = current_entry[11]
                    end_score = current_entry[13]
                    country = current_entry[4]
                    if current_entry[-1].isupper():
                        qualified = current_entry[-1]
                    else:
                        qualified = ' '
                else:
                    rank = int(current_entry[0])
                    routine = current_entry[4]
                    name = current_entry[1] + ' ' + current_entry[2]
                    d = current_entry[7]
                    e = current_entry[5]
                    t = current_entry[6]
                    h = current_entry[8]
                    pen = current_entry[11]
                    total = current_entry[10]
                    end_score = current_entry[12]
                    country = current_entry[3]
                    if current_entry[-1].isupper():
                        qualified = current_entry[-1]
                    else:
                        qualified = ' '

                    if routine == '1':
                        routine = '1st'

                df.loc[df_pos] = (rank,
                                routine,
                                name,
                                d, 
                                e,
                                t,
                                h,
                                pen,
                                total,
                                end_score,
                                country,
                                qualified
                                )  
                
                df_pos += 1
                if len(corrected_entry) < 8:
                    routine = corrected_entry[0]
                    d = 0.00
                    e = 0.00
                    t = 0.00
                    h = 0.00
                    pen = 0.00
                    total = 0.00
                    end_score = current_entry[11]
                elif len(current_entry) < 13:
                    routine = corrected_entry[0]
                    d = corrected_entry[3]
                    e = corrected_entry[1]
                    t = corrected_entry[2]
                    h = corrected_entry[4]
                    pen = corrected_entry[7]
                    total = corrected_entry[6]
                    end_score = current_entry[11]
                else:
                    routine = corrected_entry[0]
                    d = corrected_entry[3]
                    e = corrected_entry[1]
                    t = corrected_entry[2]
                    h = corrected_entry[4]
                    pen = corrected_entry[7]
                    total = corrected_entry[6]
                    end_score = current_entry[12]

                if routine == '2':
                    routine = '2nd'

                df.loc[df_pos] = (rank,
                                routine,
                                name,
                                d, 
                                e,
                                t,
                                h,
                                pen,
                                total,
                                end_score,
                                country,
                                qualified
                                )  
                
                df_pos += 1
                # header = ("Rank", "Routine", "Name", "D", "E", "T", "H", "Pen.", "Total", "End", "Country", "Qualified")
            df.to_csv(output_name + ".csv", index=False)
        elif event_phase == 'semi':
            header = ("Rank", "Name", "D", "E", "T", "H", "Pen.", "Total", "Country", "Qualified")
            df = pd.DataFrame(columns=header)

            df_pos = 0
            for entry in entry_counts:

                current_entry = Lines[entry].strip().split()

                if len(current_entry) < 11:
                    rank = int(current_entry[0])
                    name = current_entry[1] + ' ' + current_entry[2]
                    d = 0.00
                    e = 0.00
                    t = 0.00
                    h = 0.00
                    pen = 0.00
                    total = 0.00
                    country = current_entry[3]
                    if current_entry[-1].isupper():
                        qualified = current_entry[-1]
                    else:
                        qualified = ' '
                elif current_entry[3].isupper() == False:
                    rank = int(current_entry[0])
                    name = current_entry[1] + ' ' + current_entry[2] + ' ' + current_entry[3]
                    d = current_entry[8]
                    e = current_entry[6]
                    t = current_entry[7]
                    h = current_entry[9]
                    pen = current_entry[10]
                    total = current_entry[11]
                    country = current_entry[4]
                    if current_entry[-1].isupper():
                        qualified = current_entry[-1]
                    else:
                        qualified = ' '
                else:
                    rank = int(current_entry[0])
                    name = current_entry[1] + ' ' + current_entry[2]
                    d = current_entry[7]
                    e = current_entry[5]
                    t = current_entry[6]
                    h = current_entry[8]
                    pen = current_entry[9]
                    total = current_entry[10]
                    country = current_entry[3]
                    if current_entry[-1].isupper():
                        qualified = current_entry[-1]
                    else:
                        qualified = ' '


                df.loc[df_pos] = (rank,
                                  name,
                                  d, 
                                  e,
                                  t,
                                  h,
                                  pen,
                                  total,
                                  country,
                                  qualified
                                )  
                
                df_pos += 1
                # header = ("Rank", "Routine", "Name", "D", "E", "T", "H", "Pen.", "Total", "End", "Country", "Qualified")
            df.to_csv(output_name + ".csv", index=False)
        elif event_phase == 'final':
            header = ("Rank", "Name", "D", "E", "T", "H", "Pen.", "Total", "Country")
            df = pd.DataFrame(columns=header)

            df_pos = 0
            for entry in entry_counts:

                corrector = 1
                current_entry = Lines[entry].strip().split()
                corrected_entry = Lines[entry+corrector].strip().split()

                if len(current_entry) < 11:
                    rank = int(current_entry[0])
                    name = current_entry[1] + ' ' + current_entry[2]
                    d = 0.00
                    e = 0.00
                    t = 0.00
                    h = 0.00
                    pen = 0.00
                    total = 0.00
                    country = current_entry[3]
                elif current_entry[3].isupper() == False:
                    rank = int(current_entry[0])
                    name = current_entry[1] + ' ' + current_entry[2] + ' ' + current_entry[3]
                    d = current_entry[8]
                    e = current_entry[6]
                    t = current_entry[7]
                    h = current_entry[9]
                    pen = current_entry[10]
                    total = current_entry[11]
                    country = current_entry[4]
                else:
                    rank = int(current_entry[0])
                    name = current_entry[1] + ' ' + current_entry[2]
                    d = current_entry[7]
                    e = current_entry[5]
                    t = current_entry[6]
                    h = current_entry[8]
                    pen = current_entry[9]
                    total = current_entry[10]
                    country = current_entry[3]


                df.loc[df_pos] = (rank,
                                  name,
                                  d, 
                                  e,
                                  t,
                                  h,
                                  pen,
                                  total,
                                  country
                                 )   
                
                df_pos += 1
            df.to_csv(output_name + ".csv", index=False)
                # header = ("Rank", "Routine", "Name", "D", "E", "T", "H", "Pen.", "Total", "End", "Country", "Qualified")
