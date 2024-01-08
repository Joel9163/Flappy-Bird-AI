import pygame
import os
import Bird
import Pipe
import neat

pygame.font.init()
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800
STAT_FONT = pygame.font.SysFont("Ariel", 50)
FPS= 30
MAX_SCORE = 50
Jump_threshold = 0.6
punishment = -1
pygame.display.set_caption("Flappy Bird")
gen = 0
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
#initialize images
BIRD_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bird.png")).convert_alpha())
PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","pipe.png")).convert_alpha())
BACKGROUND_IMG = pygame.transform.scale(pygame.image.load(os.path.join("imgs","bg.png")).convert_alpha(), (600, 900))

def draw(SCREEN, birds, pipes, score, gen):
    SCREEN.blit(BACKGROUND_IMG, (0,0))

    for pipe in pipes:
        pipe.draw(SCREEN)

    for bird in birds:
        bird.draw(SCREEN)

    score_label = STAT_FONT.render("Score: " + str(score),1,(255,255,255))
    SCREEN.blit(score_label, (SCREEN_WIDTH - score_label.get_width() - 15, 10))

    score_label = STAT_FONT.render("Gens: " + str(gen-1),1,(255,255,255))
    SCREEN.blit(score_label, (10, 10))

    pygame.display.update()

def main(genomes, config):
    global SCREEN, gen
    SCREEN = SCREEN
    gen += 1
    score = 0
    clock = pygame.time.Clock()

    cur = Bird.Bird(230,350, BIRD_IMG)
    models = [] #create an empty list to store all the training neural networks
    genomes_list = [] #create an empty list to store all the training genomes
    birds = [] 
    pipes = [Pipe.Pipe(700, PIPE_IMG)]

    for genome_id, genome in genomes:
        birds.append(Bird.Bird(230,350, BIRD_IMG))
        genome.fitness = 0 
        model = neat.nn.FeedForwardNetwork.create(genome, config) #set up the neural network
        models.append(model)
        genomes_list.append(genome)
    
    gameloop = True
    while gameloop and len(birds) > 0:
        clock.tick(FPS)
        # if we close the window stop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameloop = False
                pygame.quit()
                quit()
                break
        
        if score >= MAX_SCORE:
            gameloop = False
            break
        
        passed_pipes = []
        add_pipe = False
        for pipe in pipes:
            pipe.move()
            for index, bird in enumerate(birds):
                if pipe.collide(bird, SCREEN):
                    genomes_list[index].fitness -= 1
                    models.pop(index)
                    genomes_list.pop(index)
                    birds.pop(index)

            if pipe.x + pipe.img.get_width() < 0:
                passed_pipes.append(pipe)
            if not pipe.passed and pipe.x < cur.x:
                pipe.passed = True
                score += 1
                add_pipe = True
        if add_pipe:    
            pipes.append(Pipe.Pipe(SCREEN_WIDTH,PIPE_IMG))
        for pipe in passed_pipes:
            pipes.remove(pipe)

        pipe_index = 0
        if len(birds) > 0:
            if len(pipes) > 1 and birds[0].x > pipes[0].x + pipes[0].img.get_width():  # determine whether to use the first or second
                pipe_index = 1 

        for index, bird in enumerate(birds):
            genomes_list[index].fitness += 0.1
            bird.move() 

            delta_x = bird.x - pipes[pipe_index].x 
            delta_y_top = bird.y - pipes[pipe_index].height 
            delta_y_bottom = bird.y - pipes[pipe_index].bottom

            #input the bird's distance from the pipes
            output = models[index].activate((delta_x, delta_y_top, delta_y_bottom))
            
            if output[0] > Jump_threshold: #if the model output is greater than the probability threshold
                bird.jump()
            
            # kill birds if they go off screen
            if bird.y + bird.img.get_height() >= 800 or bird.y < -50:
                models.pop(birds.index(bird))
                genomes_list.pop(birds.index(bird))
                birds.pop(birds.index(bird))
        
    
        draw(SCREEN, birds, pipes, score, gen)


def train(config_file):
    config = neat.config.Config(neat.DefaultGenome,
                                neat.DefaultReproduction,
                                neat.DefaultSpeciesSet,
                                neat.DefaultStagnation,
                                config_file)

    neat_pop = neat.Population(config)

    #show the statistics
    neat_pop.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    neat_pop.add_reporter(stats)

    # Run for up to 50 generations.
    winner = neat_pop.run(main, 50)

    # show final stats
    print('\nBest genome:\n{!s}'.format(winner))


local_dir = os.path.dirname(__file__)
config_path = os.path.join(local_dir, 'config.txt')
train(config_path)
    