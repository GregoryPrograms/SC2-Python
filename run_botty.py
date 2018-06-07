from pysc2.env.sc2_env import SC2Env

def make_env(id=0, **kwargs):
    env = SC2Env(**kwargs)

def train_botty():
    pass

def main():
    flags.DEFINE_string("map_name", "MoveToBeacon", "Name of the map")
    flags.DEFINE_integer("frames", 40, "Number of frames in millions")
    flags.DEFINE_integer("step_mul", 8, "sc2 step multiplier")
    flags.DEFINE_integer("n_envs", 1, "Number of sc2 environments to run in parallel")
    flags.DEFINE_integer("resolution", 32, "sc2 resolution")
    flags.DEFINE_string("lrschedule", "constant",
                        "linear or constant, learning rate schedule for baselines a2c")
    flags.DEFINE_float("learning_rate", 3e-4, "learning rate")
    flags.DEFINE_boolean("visualize", False, "show pygame visualisation")
    flags.DEFINE_float("value_weight", 1.0, "value function loss weight")
    flags.DEFINE_float("entropy_weight", 1e-5, "entropy loss weight")

    FLAGS(sys.argv)
    train_botty()

if __name__ == '__main__':
    import sys
    from absl import flags
    FLAGS = flags.FLAGS
    FLAGS(sys.argv)