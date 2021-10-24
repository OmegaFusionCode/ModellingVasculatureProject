object MyApp {

    def main(args: Array[String]): Unit = {

        val net = InvasionPercolationNetwork.make(30, 30, 0.4.toFloat)
        println("reached")
        println(net.toString)

    }

}
