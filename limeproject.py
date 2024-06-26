from enum import Enum
from os.path import isfile, isdir
from os import mkdir
import yaml, io

class LiMEProjectKey(Enum):
	C = 0
	CSharp = 1
	D = 2
	DSharp = 3
	E = 4
	F = 5
	FSharp = 6
	G = 7
	GSharp = 8
	A = 9
	ASharp = 10
	B = 11
	def fromStr(s: str):
		match s:
			case "C": return LiMEProjectKey.C
			case "C#": return LiMEProjectKey.CSharp
			case "D": return LiMEProjectKey.D
			case "D#": return LiMEProjectKey.DSharp
			case "E": return LiMEProjectKey.E
			case "F": return LiMEProjectKey.F
			case "F#": return LiMEProjectKey.FSharp
			case "G": return LiMEProjectKey.G
			case "G#": return LiMEProjectKey.GSharp
			case "A": return LiMEProjectKey.A
			case "A#": return LiMEProjectKey.ASharp
			case "B": return LiMEProjectKey.B
		return None
	def __str__(self):
		match self:
			case LiMEProjectKey.C: return "C"
			case LiMEProjectKey.CSharp: return "C#"
			case LiMEProjectKey.D: return "D"
			case LiMEProjectKey.DSharp: return "D#"
			case LiMEProjectKey.E: return "E"
			case LiMEProjectKey.F: return "F"
			case LiMEProjectKey.FSharp: return "F#"
			case LiMEProjectKey.G: return "G"
			case LiMEProjectKey.GSharp: return "G#"
			case LiMEProjectKey.A: return "A"
			case LiMEProjectKey.ASharp: return "A#"
			case LiMEProjectKey.B: return "B"
		return None

class LiMEProjectTrackItem:
	def __init__(self, using: str, position: float, length: float):
		self.using = using
		self.position = position
		self.length = length

class LiMEProjectTrack:
	def __init__(self, name: str, volume: float, items: list[LiMEProjectTrackItem]):
		self.name = name
		self.volume = volume
		self.items = items

class LiMEProject:
	def __init__(self, projectPath: str, fullName: str, author: str, iconPath: str, key: LiMEProjectKey, major: bool, bpm: float, audio: dict[str, str], tracks: list[LiMEProjectTrack]):
		self.path = projectPath
		self.fullName = fullName
		self.author = author
		self.iconPath = iconPath
		self.key = key
		self.major = major
		self.bpm = bpm
		self.audio = audio
		self.tracks = tracks
	
	def formProjDir(projectID: str):
		return "/".join(__file__.replace("\\", "/").split("/")[0:-1]) + "/projects/" + projectID + "/"
	def formProjFullPath(projectID: str):
		return LiMEProject.formProjDir(projectID) + "limeproj.yaml"

	def default(projectName: str, author: str):
		return LiMEProject(projectName, projectName, author, "", LiMEProjectKey.C, True, 120.0, {}, [])

	def create(projectName: str | None, author: str | None = None):
		if projectName == None: projectName = "New Project"
		if author == None: author = ""
		if not isdir(LiMEProject.formProjDir(projectName)):
			print(f"WARN: project '{projectName}' does not exist, attempting to create a new one")
			return LiMEProject.default(projectName, author)
		if not isfile(LiMEProject.formProjFullPath(projectName)):
			print(f"ERROR: project file for '{projectName}' does not exist")
			return None

		projectHandle = io.open(LiMEProject.formProjFullPath(projectName))
		projectYaml = yaml.safe_load(projectHandle)
		return LiMEProject.createFromYaml(projectName, projectYaml)
	
	def createFromYaml(path: str, yamlData):
		#print(yamlData)
		i = yamlData["info"]
		audio = {}
		tracks = []

		for fl in yamlData["audio"]:
			audio[fl] = yamlData["audio"][fl]

		for track in yamlData["placement"]:
			trackItems = []
			for item in track["items"]:
				trackItems.append(LiMEProjectTrackItem(item["using"], item["position"], item["length"]))

			tracks.append(LiMEProjectTrack(track["trackName"], track["volume"], trackItems))

		key = LiMEProjectKey.fromStr(i["key"]["note"])
		return LiMEProject(path, i["fullName"], i["author"], i["icon"], key, i["key"]["major"], i["bpm"], audio, tracks)
	
	def save(self):
		dirpath = LiMEProject.formProjDir(self.path)
		path = dirpath + "limeproj.yaml"
		if not isdir(dirpath):
			mkdir(dirpath)
			mkdir(dirpath + "data")
		handle = io.open(path, "w" if isfile(path) else "x")
		yaml.dump({
			"info": {
				"fullName": self.fullName,
				"author": self.author,
				"icon": self.iconPath,
				"key": {"note": str(self.key), "major": self.major},
				"bpm": self.bpm
			},
			"audio": self.audio,
			"placement": [{
				"trackName": track.name,
				"volume": track.volume,
				"items": [{
					"using": item.using,
					"position": item.position,
					"length": item.length
				} for item in track.items]
			} for track in self.tracks]
		}, handle)
		handle.close()
