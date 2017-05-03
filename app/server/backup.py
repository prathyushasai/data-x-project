@app.route('/video', methods=['POST'])
# def json_handler():

#     reqData = json.loads(request.data)
#     youtube_id = frame.get_youtube_id(reqData['url'])
#     filename = cacheFolder + "/" + youtube_id + ".json"
#     print (filename)
#     try:
#         cached = open(filename, 'r')
#         print("Found %s in JSON cache" % (filename))
#         resJson = cached.read()
#         # print (resJson)
#         resData = json.loads(resJson)
#     except:
#         print("Didn't find %s in JSON cache: %s" % (filename, str(sys.exc_info())) )
#         print (reqData['url'])
#         frames, _ = frame.extract_files(reqData['url'])
#         frames = [x[0] for x in frames]
#         print ("%d frame%s" % (len(frames), '' if len(frames) == 1 else 's'))

#         resData = {"labels" : {}}

#         global createdGraph
#         if not createdGraph:
#             print("Creating graph for the first time")
#             classifier.create_graph()
#             createdGraph = True

#         # Add important frames to resData
#         for t, f in enumerate(frames):
#             img_str = imageio.imwrite(imageio.RETURN_BYTES, f, format="jpg")
#             top_predictions, all_predictions = classifier.get_top_predictions_jpg_data(img_str, 1)

#             for node_id in top_predictions:
#                 human_string = node_lookup.id_to_string(node_id)
#                 score = np.asscalar(all_predictions[node_id])

#                 # Add to response data if above a certain threshold
#                 if human_string not in resData["labels"]:
#                     resData["labels"][human_string] = {"times" : [],
#                                                         "scores" : [],
#                                                         "labelId" : node_lookup.string_to_id(human_string)}
#                 resData["labels"][human_string]["times"].append(t)
#                 resData["labels"][human_string]["scores"].append(score)
#                 print('frame %d %s (score = %.5f)' % (t, human_string, score))

#         # Response data should be formatted like this.
#         # resData = {
#         #     "labels": {
#         #         "cat" : {
#         #             "labelId" : "n02121620",
#         #             "times": [40,50,60,70],
#         #             "scores" : [0.8, 0.3, 0.4, 0.9]
#         #         },
#         #         "dog" : {
#         #             "labelId" : "n03218446",
#         #             "times": [120,130,140]
#         #             "scores" : [0.8, 0.3, 0.4]
#         #         }
#         #     }
#         # }


#         # Remove any consecutive label times
#         items = resData["labels"].items()
#         for label, obj in items:
#             start = 1
#             times = obj["times"]
#             scores = obj["scores"]
#             for i in range(1, len(times), 1):
#                 if times[i] - times[i-1] > 1:
#                     times[start] = times[i]
#                     scores[start] = scores[i]
#                     start = start + 1
#                 else:
#                     # stick the higher value into the one we're keeping for this label
#                     if scores[i] > scores[start-1]:
#                         scores[start-1] = scores[i]
#             obj["times"] = times[:start]
#             obj["scores"] = scores[:start]

#         print(resData)
#         resJson = json.dumps(resData)
#         cached = open(filename, 'w')
#         cached.write(resJson)
#     else:
#         # See if this cached file has the labelId attribute
#         items = resData["labels"].items()
#         for label, info in items:
#             good = ("labelId" in info) and isinstance(info["labelId"], str)
#             break
#         if not good:
#             resData["youtubeId"] = youtube_id
#             items = resData["labels"].items()
#             for label, info in items:
#                 info["labelId"] = node_lookup.string_to_id(label)
#             # Write to cache
#             print("Adding nodeIds to cached data")
#             print(resData)
#             resJson = json.dumps(resData)
#             cached = open(filename, 'w')
#             cached.write(resJson)
#     pruneLabels(resData, 0.5)
#     return json.dumps(resData)