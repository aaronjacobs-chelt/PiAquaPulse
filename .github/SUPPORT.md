# Getting Support for PiAquaPulse

## Community Support Channels

### 1. GitHub Issues
- **Bug reports**: Use the bug report template
- **Feature requests**: Use the feature request template  
- **Questions**: Use GitHub Discussions
- **Hardware issues**: Include photos and sensor readings

### 2. Documentation
- [Project Documentation](../README.md)
- [Hardware Setup Guide](../SETUP.md)
- [Circuit Documentation](../Circuit%20Documentation.md)
- [Troubleshooting Guide](#troubleshooting)

## Getting Help

### Before Asking for Help
1. Check the documentation and setup guide
2. Search existing issues and discussions
3. Verify your hardware connections
4. Check the system logs for error messages
5. Test with known working sensors

### How to Ask for Help
When seeking help, please include:

1. **System Information:**
   - Raspberry Pi model (Zero W/2W)
   - OS version (`cat /etc/os-release`)
   - Python version (`python3 --version`)
   - PiAquaPulse version

2. **Hardware Setup:**
   - Sensor types and models
   - GPIO connection diagram
   - Power supply details
   - Enclosure information

3. **Problem Description:**
   - What happened vs. what you expected
   - Steps to reproduce the issue
   - When the problem started
   - Environmental conditions during testing

4. **Logs and Data:**
   - System logs from `/home/pi/PiAquaPulse/logs/`
   - Sensor readings (if available)
   - Error messages and stack traces
   - Screenshots of issues (if applicable)

### Contact Methods

1. **Bug Reports and Features:**
   - Use GitHub Issues
   - Follow the provided templates
   - Be specific and detailed

2. **General Questions:**
   - Use GitHub Discussions
   - Search existing topics first
   - Provide context about your use case

3. **Security Issues:**
   - **DO NOT** post security issues publicly
   - Email: git@aaronemail.xyz
   - Subject: "PiAquaPulse Security Issue"

4. **Hardware Support:**
   - Check hardware compatibility first
   - Include sensor datasheets
   - Provide clear connection diagrams

## Troubleshooting

### Common Issues

#### 1. Sensor Not Detected
- Verify GPIO connections match the documentation
- Check that required interfaces are enabled (SPI, I2C, 1-Wire)
- Ensure sensors have proper power supply
- Test with a multimeter if needed

#### 2. GPS Not Working
- Ensure GPS module has clear view of sky
- Check UART configuration in `/boot/config.txt`
- Verify TX/RX connections are correct
- Allow time for GPS fix (can take several minutes)

#### 3. pH Sensor Inaccurate
- Calibrate with known buffer solutions (pH 4.0, 7.0, 10.0)
- Check sensor probe condition
- Verify analog connections to MCP3008
- Temperature compensation may be needed

#### 4. Data Logging Issues
- Check file permissions in data directory
- Ensure SD card has sufficient space
- Verify CSV file format is not corrupted
- Check system time/date configuration

#### 5. Power Issues
- Monitor power consumption with sensors active
- Check battery voltage levels
- Ensure adequate power supply for all components
- Consider power-saving optimizations

### System Diagnostics

Run these commands to gather diagnostic information:

```bash
# Check system status
sudo systemctl status piaquapulse.service

# View recent logs  
sudo journalctl -u piaquapulse.service -n 50

# Check GPIO status
gpio readall

# Test SPI interface
ls /dev/spi*

# Check 1-Wire devices
ls /sys/bus/w1/devices/

# Test UART
sudo cat /dev/ttyS0
```

## Contributing

Want to help improve PiAquaPulse?

1. Read [CONTRIBUTING.md](../CONTRIBUTING.md)
2. Fork the repository
3. Submit pull requests
4. Help with documentation
5. Share your field experiences
6. Contribute sensor calibration data

## Support Guidelines

### Be Respectful
- Follow the code of conduct
- Be patient with community members
- Share knowledge and experiences
- Help others when you can

### Be Detailed
- Provide complete system information
- Show your research and attempts
- Include relevant context and use cases
- Document your findings for others

### Be Constructive
- Suggest solutions and improvements
- Test thoroughly before reporting
- Share successful configurations
- Contribute back to the community

## Commercial Support

For commercial applications, custom development, or priority support:

- **Email**: git@aaronemail.xyz
- **Subject**: "PiAquaPulse Commercial Support"

Commercial support includes:
- Custom sensor integration
- Field deployment assistance  
- Data analysis consultation
- Hardware modification services
- Training and workshops

## Field Support

### Deployment Guidelines
- Test thoroughly in lab conditions first
- Carry backup sensors and components
- Plan for power management in remote locations
- Consider environmental protection needs
- Have data backup strategies

### Emergency Contact
For critical field deployment issues:
- Email: git@aaronemail.xyz
- Subject: "PiAquaPulse Field Emergency"

Include GPS coordinates and expected response time needs.

---

**Remember**: PiAquaPulse is designed for environmental monitoring. Your field data contributes to understanding water quality - thank you for your scientific contribution! 🌊🔬

