import os
import csv
import argparse


class Skeleton:
    def __init__(self) -> None:
        self.__joints = dict()
        self.joint_names = ['SpineBase', 'SpineMid', 'Neck', 'Head', 
                            'ShoulderLeft', 'ElbowLeft', 'WristLeft', 'HandLeft',
                            'ShoulderRight', 'ElbowRight', 'WristRight', 'HandRight',
                            'HipLeft', 'KneeLeft', 'AnkleLeft', 'FootLeft',
                            'HipRight', 'KneeRight', 'AnkleRight', 'FootRight', 
                            'SpineShoulder', 'HandTipLeft', 'ThumbLeft', 'HandTipRight', 'ThumbRight']

    def __getitem__(self, key: str) -> tuple:
        if key in self.__joints:
            return self.__joints[key]
        else:
            raise KeyError("Invalid joint name: " + key)

    def __setitem__(self, key: str, value: tuple or list) -> None:
        if key in self.joint_names:
            self.__joints[key] = value
        else:
            raise KeyError("Invalid joint name: " + key)

    def __len__(self) -> int:
        return len(self.__joints)

    def __iter__(self) -> iter:
        return iter(self.__joints)

    def __contains__(self, item: str) -> bool:
        return item in self.__joints

    def __str__(self) -> str:
        return ', '.join(['{}: {}'.format(k, v) for k, v in self.__joints.items()])

    def __repr__(self) -> str:
        return str(self)

class KinectStream:
    def __init__(self, file_name: str) -> None:
        self.__file_name, self.__extension = os.path.splitext(file_name)
        self.__stream = []
        self.__read_file()

    def __read_file(self) -> None:
        with open(self.__file_name + self.__extension, 'r') as csv_file:
            reader = csv.reader(csv_file, delimiter=';')
            for row in reader:
                sk = Skeleton()
                for i, joint_name in enumerate(sk.joint_names):
                    sk[joint_name] = (float(row[i * 14]), float(row[i * 14 + 1]), float(row[i * 14 + 2]))
                self.__stream.append(sk)

    def write_file(self) -> None:
        with open(self.__file_name + '_processed' +self.__extension, 'w', newline='', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file, delimiter=',')
            row = ['Time']
            for joint_name in self.__stream[0].joint_names:
                row.extend([joint_name+'X', joint_name+'Y', joint_name+'Z'])
            writer.writerow(row)

            for t, sk in enumerate(self.__stream):
                row = [400*t]
                for joint_name in sk.joint_names:
                    row.append(sk[joint_name][0])
                    row.append(sk[joint_name][1])
                    row.append(sk[joint_name][2])
                writer.writerow(row)

    def __str__(self) -> str:
        return '\n\n'.join(['{}: {}'.format(i, sk) for i, sk in enumerate(self.__stream)])

    def __repr__(self) -> str:
        return self.__str__()

    def __len__(self) -> int:
        return len(self.__stream)

    def __iter__(self) -> iter:
        return iter(self.__stream)

    def __contains__(self, item) -> bool:
        return item in self.__stream

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('file', nargs='?', type=str, help='skeleton_ssi.csv file from nova software')
    args = parser.parse_args()

    ks = KinectStream(args.file)
    ks.write_file()
