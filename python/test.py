import planning
import ambiguity
import interpreting
import shrdlite

if __name__ == '__main__':
    tree = shrdlite.parse([
    interpreter = interpreting.Interpreter()
    goals1 = interpreter.interpret(tree)

    ambiguityResolver = ambiguity.AmbiguityResolver(world, objects)
    goal2 = ambiguityResolver.handleInput(goals1)
    
    goal2 = ("move",) + goal2
    goal2 = list(goal2)
    goal2 = [','.join(goal2)]
    print goal2
    


