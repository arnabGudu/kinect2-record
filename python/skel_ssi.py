import csv
import argparse

class Joint:
    def __init__(self, name, x, y, z):
        self.name = name
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)
    
    def __str__(self):
        return self.name + ": " + str(self.x) + ", " + str(self.y) + ", " + str(self.z)

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.name == other.name and self.x == other.x and self.y == other.y and self.z == other.z

class Skeleton:
    def __init__(self):
        self._joints = dict()
        self.joint_names = ['Head', 'Neck', 'Torso', 'HipCenter', 
                            'LShoulder', 'LElbow', 'LWrist', 'LHand',
                            'RShoulder', 'RElbow', 'RWrist', 'RHand',
                            'LHip', 'LKnee', 'LAnkle', 'LFoot',
                            'RHip', 'RKnee', 'RAnkle', 'RFoot',
                            'ShoulderSpine', 
                            'LHandTip', 'LThumb', 'RHandTip', 'RThumb']

    def __getitem__(self, key):
        return self._joints[key]

    def __setitem__(self, key, value):
        self._joints[key] = value

    def __len__(self):
        return len(self._joints)

    def __iter__(self):
        return iter(self._joints)

    def __contains__(self, item):
        return item in self._joints

class KinectStream:
    def __init__(self, file_name):
        self._file_name = file_name
        self._stream = []
        self._read_file()

    def _read_file(self):
        with open(self._file_name, 'r') as csv_file:
            reader = csv.reader(csv_file, delimiter=';')
            for row in reader:
                sk = Skeleton()
                for i, joint_name in enumerate(sk.joint_names):
                    sk[joint_name] = Joint(joint_name, row[i * 14], row[i * 14 + 1], row[i * 14 + 2])
                self._stream.append(sk)

    def write_file(self):
        with open(self._file_name + '_', 'w') as csv_file:
            writer = csv.writer(csv_file, delimiter=',')
            for sk in self._stream:
                row = []
                for joint_name in sk.joint_names:
                    row.append(sk[joint_name].x)
                    row.append(sk[joint_name].y)

    def animation(self):
        for sk in self._stream:
            for joint_name in sk.joint_names:
                print(sk[joint_name])

    def __str__(self):
        return str(self._stream)

    def __repr__(self):
        return self.__str__()

    def __len__(self):
        return len(self._stream)

    def __iter__(self):
        return iter(self._stream)

    def __contains__(self, item):
        return item in self._stream
            
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('file', nargs='?', type=str, help='file to read')
    args = parser.parse_args()
    ks = KinectStream(args.file)