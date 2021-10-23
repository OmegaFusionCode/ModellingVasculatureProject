object MyApp {

    def main(args: Array[String]): Unit = {

        val p = new InvasionPercolationNetwork(30, 30, 0.4.toFloat)
        val a = p.makeNewNetwork()
        println("reached")
        InvasionPercolationNetwork.draw(a)

    }

}
