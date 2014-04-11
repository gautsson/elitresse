# The world and the goal
world = [["e"],["g","l"],[],["k","m","f"],[]]
holding = null

# Gets all the empty stacks in the world
def getEmptyStacks(world):
	x = []
	for stack, object in enumerate(world):
		if not object:
			x.append(stack)
	return x


		
	

if __name__ == '__main__':
    	print(getEmptyStacks(world))