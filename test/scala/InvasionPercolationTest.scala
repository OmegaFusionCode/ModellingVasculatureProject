import org.scalatest.funsuite.AnyFunSuite


class InvasionPercolationTest extends AnyFunSuite {
    test("The number of filled cells is correct") {
        val r = scala.util.Random
        for (_ <- 1 to 20) {
            val x = 1 + r.nextInt(30)
            val y = 1 + r.nextInt(30)
            val occupancy = r.nextFloat()
            val expectedCount = scala.math.round(x * y * occupancy)
            val network = InvasionPercolationNetwork.make(x, y, occupancy)
            //assert(expectedCount === network.numToFill)
            var total = 0
            for (row <- network.cells) for (c <- row)
                if (c.isReached) total += 1
            assert(expectedCount === total)
        }
    }

    test("All cells were discovered before they were reached") {
        val r = scala.util.Random
        for (_ <- 1 to 20) {
            val x = 1 + r.nextInt(30)
            val y = 1 + r.nextInt(30)
            val occupancy = r.nextFloat()
            val network = InvasionPercolationNetwork.make(x, y, occupancy)
            for (i <- 0 until x) for (j <- 0 until y) {
                val c = network.cells(i)(j)
                assert(c.reached == -1 || c.discovered < c.reached)
            }
        }
    }

    test("Each cell was discovered on the same step that its parent was reached") {

        def hasParent(network: InvasionPercolationNetwork, c: InvasionPercolationNetwork.Cell): Boolean = {
            val i = c.i
            val j = c.j
            val x = network.cells.length
            val y = network.cells(0).length
            val neighbours = List((i-1, j), (i+1, j), (i, j-1), (i, j+1))
            for ((i2, j2) <- neighbours if i2 >= 0 && j2 >= 0 && i2 < x && j2 < y) {
                val d = network.cells(i2)(j2)
                // If d was reached when c was discovered, then d is c's parent.
                if (d.reached == c.discovered) return true
            }
            false
        }

        val r = new scala.util.Random()
        for (i <- 1 to 20) {
            val x = 1 + r.nextInt(30)
            val y = 1 + r.nextInt(30)
            val occupancy = r.nextFloat()
            val network = InvasionPercolationNetwork.make(x, y, occupancy)
            for (i <- 0 until x) for (j <- 0 until y) {
                val c = network.cells(i)(j)
                // Note that the initial node does not have a parent.
                assert(hasParent(network, c) || c.discovered == 0)
            }
        }
    }
}
